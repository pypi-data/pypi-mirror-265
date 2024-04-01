# ---------------------------------#
# ------- VIDEO SESSION -----------#
# ---------------------------------#
from abc import abstractmethod
from io import BytesIO
import logging
import zlib
import tempfile
import glob
import os
import logging
import pandas as pd
import numpy as np

from PIL import Image
from zipfile import ZipFile
from pyspark.sql.types import StructField, StructType, IntegerType, BinaryType, StringType, TimestampType, FloatType, \
    LongType
from petastorm.unischema import dict_to_spark_row, Unischema, UnischemaField
from petastorm.etl.dataset_metadata import materialize_dataset

from cads_sdk.nosql.codec import *
from cads_sdk.nosql.utils import get_size_of_dir,get_size_of_list,check_delta,replace_special_characters
from cads_sdk.nosql.base import ConvertFromFolder, ConvertToFolder

try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 opencv-python")
    import cv2

    OPENCV_AVAILABLE = False


class ConvertFromFolderVideo(ConvertFromFolder):
    def __init__(
            self,
            input_path,
            input_type,
            output_path,
            table_name='',
            database='',
            repartition=True,
            numPartition=None,
            file_format='parquet',
            compression='zstd',
            input_recursive=True,
            thumbnail_width=256,
            thumbnail_height=144,

            shorten=False,

            debug=False
    ):
        super().__init__(input_path=input_path,
                         input_type=input_type,
                         output_path=output_path,
                         table_name=table_name,
                         database=database,
                         repartition=repartition,
                         numPartition=numPartition,
                         file_format=file_format,
                         compression=compression,
                         input_recursive=input_recursive,
                         shorten=shorten,
                         debug=debug)

        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height

    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""
        for row in partitionData:
            path = row.path
            if self.debug:
                print(f"Convert video {path}")  # , file=self.log_file)

            cap = cv2.VideoCapture(path)
            frame_size = (int(cap.get(3)), int(cap.get(4)))
            frame_number = cap.get(cv2.CAP_PROP_FRAME_COUNT) / 2
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
            res, frame = cap.read()
            frame = cv2.resize(frame, (self.thumbnail_width, self.thumbnail_height))
            # frame = frame[:, :, (2, 1, 0)]
            duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)

            row_dict = {
                'path': path,
                'thumbnail': frame,
                'duration': duration,
                'frame_size': str(frame_size),
                'video': open(path, "rb").read()}

            yield dict_to_spark_row(self.unischema, row_dict)

    def get_schema(self):
        return Unischema('VideoShema', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('thumbnail', np.uint8, (self.thumbnail_height, self.thumbnail_width, 3),
                           CompressedImageCodec('.jpg'), False),
            UnischemaField('duration', np.float_, (), ScalarCodec(FloatType()), False),
            UnischemaField('frame_size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('video', np.bytes_, (), VideoCodec(), False)
        ])

    def execute(self, ROWGROUP_SIZE_MB=256):
        input_files = sorted(glob(self.input_path, recursive=self.input_recursive))
        self.output_path = self.convert_to_hdfs_path(self.output_path)

        spark = self.get_spark()
        Schema = self.get_schema()

        if input_files:
            input_files = self._generate_input_files()
            self.analyze_path = input_files
            self.numPartition = self.get_num_partition()
            self.output_path = self.convert_to_hdfs_path(self.output_path)
            output_path = self._generate_output_path()
            table_name = self._generate_table_name()
            Schema = self.get_schema()
            spark = self.get_spark()

            self.write_to_path(spark_df=self.create_dataframe(spark=spark,
                                                              Schema=Schema,
                                                              input_files=input_files),

                               output_path=self.output_path,
                               table_name=self.table_name,
                               database=self.database,
                               numPartition=self.numPartition,
                               compression=self.compression)

            if self.shorten:
                Schema.__dict__['_fields']['rel_path'] = UnischemaField('rel_path', np.str_, (),
                                                                        ScalarCodec(StringType()), False)
                Schema.__dict__['rel_path'] = UnischemaField('rel_path', np.str_, (), ScalarCodec(StringType()), False)
            with materialize_dataset(spark, self.output_path, Schema, ROWGROUP_SIZE_MB):
                print("Write metadata")

        else:
            logging.warn("No files were found, check your input_path")

        logging.info("Convert complete")


class ConvertFromVideo2Image:
    """
    Create a parquet/delta file given local Video file


    Parameters
    ----------
    input_path : unicode, str
        The input filename include ``mp4``
        Just only 1 video at the time

        Examples:
        input_path="**/*.mp4"

    output_path : unicode
        Ouput directory location maybe file:/ (local file) or hdfs:/ (datalake path)

        Examples:
        output_path = "file:/home/username/"
        output_path = "hdfs:/user/username/"

    table_name : str
        Table_name store metadata
        User should input table_name follow dwh convention: img_abc, vid_abc, audio_abc

        Examples: img_abc

    database : str
        Database to store metadata
        User should input database follow dwh convention: default

        Examples: default


    repartition : bool
        Default: False
        Data will be repartition to target file size

    numPartition : int
        Default None
        Number of part each user want to seperate parquet file into

    file_format : str
        Default: parquet
        File format user want to write parquet/delta

    compression: str
        Default: zstd
        Compression method user want to compress parquet file
        Value: None, zstd, snappy
        See spark.sql.parquet.compression.codec
        https://spark.apache.org/docs/2.4.3/sql-data-sources-parquet.html

    image_type: str
        Default: jpg
        Value png or jpg

    image_color : int
        Default: 3
        Value 3, 2 or 1, shape of image have color is 3 or 1 if gray image

    size : List of Tuple
        Default: jpg
        List size user want to resize or padding
        Examples: size = [(320, 180), (500, 100)]

    resize_mode : str
        Default: None
        Value: None, padding, resize
        Mode of image user want to resize
        If in folder user have various size of image, 300, 400 500

        User will add size = 500:
        And resize_mode  = 'padding'

        Then function will convert all image 300, 400, 500 to shape of 500

    input_recursive : bool
        Default: True

        If True:
        will loop through folder to get all pattern

    debug : bool

        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    >>> from cads_sdk.nosql.video import ConvertFromVideo2Image
    >>> converter = ConvertFromVideo2Image(
    >>>               input_path='/home/username/image_storage/vid/palawan1.mp4',
    >>>               input_recursive = False,
    >>>               output_path = f"file:/home/username/image_storage/vid_image.parquet",
    >>>              )
    >>>
    >>> converter.execute()

    Function will convert palawan1.mp4 to /home/username/image_storage/vid_image.parquet
    """

    def __init__(
            self,
            input_path,
            output_path,
            table_name='',
            database='',
            repartition=True,
            numPartition=None,
            file_format='parquet',
            compression='zstd',
            input_recursive=False,
            thumbnail_width=280,
            thumbnail_height=720,

            debug=False
    ):

        self.input_path = input_path
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.input_recursive = input_recursive
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format

        self.thumbnail_width = thumbnail_width
        self.thumbnail_height = thumbnail_height

        self.debug = debug

        if debug:
            self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')
            self.tmp_file = os.path.join(self.temp_folder.name, 'sdk.log')
            self.log_file = open(self.tmp_file, 'w+')
            logging.basicConfig(level=logging.DEBUG, filename=self.tmp_file, filemode='w+')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(
                    input_path.replace("hdfs:", ""))
            else:
                return input_path

    def coalesce_dataframe(self, spark_df, numPartition):
        if numPartition:
            return spark_df.coalesce(numPartition)
        return spark_df

    def write_to_path(self, spark_df, output_path, table_name='', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'parquet'
        else:
            file_format = 'delta'

        if "file:" in output_path:
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .save()
        else:
            if table_name == '' or database == '':
                raise ValueError("You must add table_name and database")
            self.coalesce_dataframe(spark_df, numPartition).write \
                .format(file_format) \
                .option('compression', compression) \
                .mode('overwrite') \
                .option("path", output_path) \
                .saveAsTable(database + '.' + table_name)

        if file_format == 'delta':
            ss.sql(f"""
            OPTIMIZE delta.`{output_path}` ZORDER BY(1)
            """)

            ss.sql(f"""
            VACCUUM delta.`{output_path}` RETAINS 0 HOURS
            """)

    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""
        for row in partitionData:
            frame_id = row.frame_id
            if self.debug:
                print(f"Convert video {frame_id}")  # , file=self.log_file)

            cap = cv2.VideoCapture(row.path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id - 1)
            res, frame = cap.read()
            # frame = cv2.resize(frame, (self.thumbnail_width, self.thumbnail_height))
            # frame = frame[:, :, (2, 1, 0)]

            row_dict = {
                'frame_id': row.frame_id,
                'path': row.path,
                'duration': row.duration,
                'frame_size': row.frame_size,
                'total_frame': row.total_frame,
                'frame': frame
            }

            yield dict_to_spark_row(self.unischema, row_dict)

    def create_dataframe(self, spark, Schema, input_files):
        path = input_files
        cap = cv2.VideoCapture(path)
        frame_size = (int(cap.get(3)), int(cap.get(4)))
        duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        pdf = pd.DataFrame(range(int(total_frame)), columns=['frame_id'])
        pdf['path'] = path
        pdf['duration'] = duration
        pdf['frame_size'] = str(frame_size)
        pdf['total_frame'] = total_frame

        spark_df = spark.createDataFrame(pdf)
        self.unischema = Schema

        self.thumbnail_width = frame_size[0]
        self.thumbnail_height = frame_size[1]

        return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())

    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark

    def get_schema(self):
        return Unischema('VideoImage', [
            UnischemaField('frame_id', np.int, (), ScalarCodec(IntegerType()), False),
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('duration', np.float_, (), ScalarCodec(FloatType()), False),
            UnischemaField('frame_size', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('total_frame', np.str_, (), ScalarCodec(FloatType()), False),
            UnischemaField('frame', np.uint8, (self.thumbnail_height, self.thumbnail_width, 3),
                           CompressedImageCodec('.jpg'), False),
        ])

    def execute(self):
        ROWGROUP_SIZE_MB = 256
        input_files = self.input_path  # sorted(glob(self.input_path, recursive=self.input_recursive))
        self.output_path = self.convert_to_hdfs_path(self.output_path)

        spark = self.get_spark()
        Schema = self.get_schema()

        if input_files:
            logging.info(f"Write at path: {self.output_path}")
            logging.info(f"Save metadata at: {self.table_name}")

            self.write_to_path(spark_df=self.create_dataframe(spark=spark,
                                                              Schema=Schema,
                                                              input_files=input_files),

                               output_path=self.output_path,
                               table_name=self.table_name,
                               database=self.database,
                               numPartition=self.numPartition,
                               compression=self.compression)
            if self.shorten:
                Schema.__dict__['_fields']['rel_path'] = UnischemaField('rel_path', np.str_, (),
                                                                        ScalarCodec(StringType()), False)
                Schema.__dict__['rel_path'] = UnischemaField('rel_path', np.str_, (), ScalarCodec(StringType()), False)
            with materialize_dataset(spark, self.output_path, Schema, ROWGROUP_SIZE_MB):
                print("Write metadata")
        else:
            logging.warn("No files were found, check your input_path")

        logging.info("Convert complete")


class ConvertToFolderVideo(ConvertToFolder):
    """
    Create a folder Video given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame


    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input filename to load video or dataframe include video

    input_path : unicode
        Path to a local file or hdfs file containing the video.

    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a video file (mp4, ts...)

    write_mode : str
        Specify the write_mode user want to

        If write_mode = 'recovery'
        Function will convert video to a multiple level of directory base on column path

        If write_mode != 'recovery'
        Function will convert all video in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
        Glob path that user input when use ConvertFromFolderVideo function

        For example: "/home/username/image_storage/audio_mp3/*.mp3"

        When output it will replace '/home/username/image_storage/audio_mp3/'  by ''

        That turn column path from absolute path to relative path

    debug : bool

        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    >>> from cads_sdk.nosql.video import ConvertToFolderVideo
    >>> converter = ConvertToFolderVideo(
    >>> input_path = 'file:/home/username/image_storage/vid.parquet',
    >>> output_path = './abc'
    >>> )
    >>>
    >>> converter.execute()

    Function will convert all video in file:/home/username/image_storage/vid.parquet to relative directory ./abc
    """

    def __init__(
            self,
            data=None,
            input_path: str = None,
            output_path: str = './output',
            write_mode="recovery",
            raw_input_path="",
            debug=False
    ):
        super().__init__(data=data,
                         input_path=input_path,
                         output_path=output_path,
                         write_mode=write_mode,
                         raw_input_path=raw_input_path,
                         debug=debug)

    def write_to_folder(self, row=None):
        if self.write_mode == "recovery":
            output_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            output_path = os.path.join(self.output_path, base_path)
        if self.debug:
            logging.info(output_path)
        with open(output_path, 'wb') as wfile:
            wfile.write(row.video)