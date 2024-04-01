import os
import logging
import pandas as pd
import numpy as np
from PIL import Image
from zipfile import ZipFile
from pyspark.sql.types import StructField, StructType, IntegerType, BinaryType, StringType, TimestampType, FloatType, \
    LongType
from petastorm.etl.dataset_metadata import materialize_dataset

from cads_sdk.nosql.codec import *
from cads_sdk.nosql.utils import get_size_of_dir,get_size_of_list,check_delta,replace_special_characters
from cads_sdk.nosql.base import ConvertFromFolder, ConvertToFolder
from cads_sdk.nosql.etl import padding
import cads_sdk as ss


try:
    import cv2

    OPENCV_AVAILABLE = True
except ImportError:
    os.system("pip install --proxy http://proxy.hcm.fpt.vn:80 opencv-python")
    import cv2

    OPENCV_AVAILABLE = False


class ConvertFromFolderImage(ConvertFromFolder):
    """
    Create a parquet/delta file given local Image directory


    Parameters
    ----------
    input_path : unicode, str
        The input filename include ``png``, ``jpeg`` image
        User can add system file pattern like *

        Examples:
        input_path="./path"
        input_path="/home/username/path"

    input_type : unicode, str
        str: 'jpg'
        or
        type: ('jpg', 'png')

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

        IF user want to query table and filter faster: use delta

        Function will auto optimize dataframe to best practice partition size and ZOrder by path

    compression: str
        Default: zstd
        Compression method user want to compress parquet file

        Value: None, zstd, snappy

        See spark.sql.parquet.compression.codec
        https://spark.apache.org/docs/2.4.3/sql-data-sources-parquet.html

    image_type: str
        Default: jpg

        Value png or jpg
        Or ('png', 'jpg')

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

    shorten : bool
        Default: False

        If True:
        Create a column shorten of path that can be filter more quickly

    debug : bool

        If debug=True:
        Write log into sdk.log file and print more debug information

    Examples
    --------
    >>> from cads_sdk.nosql.image import ConvertFromFolderImage
    >>> converter = ConvertFromFolderImage(
    >>>               input_path="/home/username/image_storage/images",
    >>>               #setting output
    >>>               output_path = f"hdfs:/user/username/image/img_images_jpg.parquet",
    >>>               table_name = 'img_images_jpg',
    >>>               database = 'default',
    >>>               file_format = 'parquet', # delta|parquet
    >>>               compression = 'zstd', # |snappy|zstd
    >>>               # setting converter
    >>>               image_type = 'jpg',
    >>>               image_color = 3,
    >>>               resize_mode="padding", # |padding|resize
    >>>               size = [(212,212),
    >>>                      (597, 597)],
    >>>               input_recursive = True, # will loop through folder to get all pattern
    >>>              )
    >>>
    >>> converter.execute()

    >>> from cads_sdk.nosql.image import ConvertFromFolderImage
    >>>
    >>> converter = ConvertFromFolderImage(
    >>>               input_path="/home/username/image_storage/device_images",
    >>>               #setting output
    >>>               output_path = f"file:/home/username/image/img_user_device_jpg.delta",
    >>>               table_name = 'img_user_device_jpg',
    >>>               database = 'default',
    >>>               file_format = 'delta', # |parquet
    >>>               compression = 'zstd', # |snappy|zstd
    >>>
    >>>               # setting converter
    >>>               image_type = 'jpg', # |'png'|('jpg', 'png')
    >>>               image_color = 3,
    >>>               resize_mode=None, # |padding|resize
    >>>               size = [(212,212),
    >>>                      (597, 597)],
    >>>               input_recursive = True, # will loop through folder to get all pattern
    >>>              )
    >>>
    >>> converter.execute()

    Function will convert all Image in file:'/home/username/device_images/' to absolute directory file:/home/username/image/img_images_jpg.parquet
    """

    def __init__(
            self,
            input_path,
            input_type,
            output_path,
            table_name='',
            database='',
            repartition=False,
            numPartition=None,
            file_format='parquet',
            compression='zstd',

            image_type='jpg',
            image_color=3,
            size=[(720, 360)],
            resize_mode=None,
            input_recursive=False,
            shorten=False,

            debug=False
    ):
        self.image_type = image_type
        self.image_color = image_color
        self.size = size
        self.resize_mode = resize_mode

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

        if isinstance(self.input_type, (tuple, list)):
            self.image_type = 'jpg'

    # specific function for image
    def _generate_output_path(self, s):
        if self.resize_mode:
            if "." + self.file_format in self.output_path:
                output_path = self.output_path.replace("." + self.file_format,
                                                       "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]),
                                                                                         file_format=self.file_format))
            else:
                output_path = self.output_path + "_{s0}_{s1}.{file_format}".format(s0=str(s[0]), s1=str(s[1]),
                                                                                   file_format=self.file_format)
        else:
            if "." + self.file_format in self.output_path:
                output_path = self.output_path
            else:
                output_path = self.output_path + f".{self.file_format}"
        logging.info(f"Write at path: {output_path}")
        return output_path

    def _generate_table_name(self, s):
        if self.resize_mode:
            if self.table_name:
                table_name = self.table_name + "_{s0}_{s1}".format(s0=str(s[0]), s1=str(s[1]))
            else:
                table_name = ''
        else:
            table_name = self.table_name
        logging.info(f"Save metadata at: {table_name}")
        return table_name

    def replace_character(self, txt):
        for i in range(len(txt)):
            if ord(txt[i]) > 1000:
                txt = txt[:i] + txt[i].encode('unicode_escape').decode('utf-8') + txt[i + 1:]
        return txt

    def create_dataframe(self,
                         spark,
                         Schema,
                         input_files,
                         size):
        from pyspark.sql.functions import expr
        self.unischema = Schema
        self.s = size
        pdf = pd.DataFrame([self.replace_character(i) for i in input_files], columns=['path'])
        spark_df = spark.createDataFrame(pdf)
        if not self.resize_mode:
            logging.warning(
                f"Not resize image, If get size error try to turn resize_mode='padding' or resize_mode='resize'")
        if self.shorten:
            return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator),
                                         Schema.as_spark_schema()).withColumn("rel_path", expr(
                f"""replace(path, '{self.commonpath}', '') """))
        else:
            return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())

    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""
        for row in partitionData:
            path = row.path
            if self.debug:
                print(f"Convert Image {path}")  # , file=self.log_file)
                print(replace_special_characters(path))
            path = replace_special_characters(path)
            try:
                img = Image.open(path)
            except Exception as e:
                print(e)
                print(path)
                img = None
            if type(img).__name__ != "NoneType":
                if self.resize_mode == 'padding':
                    row_dict = {
                        'path': path,
                        'size': img.size.__str__(),
                        'image': padding(np.array(img), (self.s[0], self.s[1]))
                    }

                    yield dict_to_spark_row(self.unischema, row_dict)
                elif self.resize_mode == 'resize':
                    row_dict = {
                        'path': path,
                        'size': img.size.__str__(),
                        'image': cv2.resize(np.array(img), (self.s[0], self.s[1]))
                    }

                    yield dict_to_spark_row(self.unischema, row_dict)
                else:
                    row_dict = {
                        'path': path,
                        'size': img.size.__str__(),
                        'image': open(path, 'rb').read()
                    }

                    yield dict_to_spark_row(self.unischema, row_dict)
            else:
                try:
                    row_dict = {
                        'path': path,
                        'size': "Can not get size",
                        'image': open(path, 'rb').read()
                    }
                except:
                    row_dict = {
                        'path': path,
                        'size': "Can not open image, image damage",
                        'image': b''
                    }

                yield dict_to_spark_row(self.unischema, row_dict)

    def get_schema(self, size, image_type, image_color):
        """
        :param size: Image size, schema need to be consistency
        :param image_type: Image type is compress JPG or PNG
        :param image_color: 3 dimention color or 1 dimention colors
        """
        if self.resize_mode:
            return Unischema('ImageSchema', [
                UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
                UnischemaField('size', np.str_, (), ScalarCodec(StringType()), False),
                UnischemaField('image', np.uint8, (size[0], size[1], image_color),
                               CompressedImageCodec(self.image_type, quality=95), False)
            ])

        else:
            return Unischema('ImageSchema', [
                UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
                UnischemaField('size', np.str_, (), ScalarCodec(StringType()), False),
                UnischemaField('image', np.bytes_, (size[0], size[1], image_color), ImageZipCodec(BinaryType()), False)
            ])

    def check_size(self, img, list_size):
        """
        Check size of image to put it in different table
        """
        for s in list_size:
            if img.shape[0] <= s[0] and img.shape[1] <= s[1]:
                return s
        self.size.append(s)
        self.dict_image[(img.shape[0], img.shape[1])] = []
        return s

    def execute(self, ROWGROUP_SIZE_MB=256):
        self.dict_image = {}
        for s in self.size:
            self.dict_image[s] = []

        if self.resize_mode:
            if len(self.size) == 0:
                raise ValueError("User must input size when using resize_mode")

            list_file = self._generate_input_files()

            # classify image into each size in list
            for p in list_file:
                img = cv2.imread(p)
                if type(img).__name__ != "NoneType":
                    self.dict_image[self.check_size(img, self.size)].append(p)
        else:
            self.dict_image[self.size[0]] = self._generate_input_files()

        for s in self.size:
            if self.dict_image[s]:
                self.analyze_path = self.dict_image[s]
                self.numPartition = self.get_num_partition()
                Schema = self.get_schema(s, self.image_type, self.image_color)
                self.output_path = self.convert_to_hdfs_path(self.output_path)
                output_path = self._generate_output_path(s)
                table_name = self._generate_table_name(s)
                spark = self.get_spark()

                with materialize_dataset(spark, output_path, Schema, ROWGROUP_SIZE_MB):
                    self.write_to_path(spark_df=self.create_dataframe(spark=spark,
                                                                      Schema=Schema,
                                                                      input_files=self.dict_image[s],
                                                                      size=s),

                                       output_path=output_path,
                                       table_name=table_name,
                                       database=self.database,
                                       numPartition=self.numPartition,
                                       compression=self.compression)

        total_files = sum([len(self.dict_image[s]) for s in self.size])
        if total_files == 0:
            logging.warn("No files were found, check your input_path or image_type")

        logging.info("Convert complete")


class ConvertFromZipImage(ConvertFromFolderImage):
    """
    Create a parquet/delta file given local Image directory


    Parameters
    ----------
    input_path : unicode, str
        The input ZIP directory include ``png``, ``jpeg`` image
        User can add system file pattern like *

        Examples:
        input_path="/path/to/MOT17.zip"
        This pattern get all jpg in folder with different directory levels
        View https://docs.python.org/3/library/glob.html

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

    image_type : str
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

    shorten : bool
        Default: False
        If True:

        Create a column shorten of path that can be filter more quickly

    debug : bool
        If debug=True:

        Write log into sdk.log file and print more debug information

    Examples
    --------
    >>> from cads_sdk.nosql.image import ConvertFromZipImage
    >>>
    >>> converter = ConvertFromZipImage(
    >>>               input_path="/home/username/image_storage/MOT17.zip",
    >>>
    >>>               #setting output
    >>>               output_path = f"hdfs:/user/username/image/img_images_jpg.parquet",
    >>>               table_name = 'img_images_jpg',
    >>>               database = 'default',
    >>>               file_format = 'parquet', # delta|parquet
    >>>               compression = 'zstd', # |snappy|zstd
    >>>               # setting converter
    >>>               image_type = 'jpg', # |'png'|('jpg', 'png')
    >>>               image_color = 3,
    >>>               resize_mode=None, # |padding|resize
    >>>               size = [(212,212)],
    >>>
    >>>               input_recursive = True, # will loop through folder to get all pattern
    >>>              )
    >>>
    >>> converter.execute()

    Function will convert all Image in file:'/home/username/image_storage/MOT17.zip' to absolute directory hdfs:/user/username/image/img_images_jpg.parquet
    """

    def __init__(
            self,
            input_path,
            input_type,
            output_path,
            table_name='',
            database='',
            repartition=False,
            numPartition=None,
            file_format='parquet',
            compression='zstd',

            image_type='jpg',
            image_color=3,
            size=[(720, 360)],
            resize_mode=None,
            input_recursive=False,

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
                         image_type=image_type,
                         image_color=image_color,
                         size=size,
                         resize_mode=resize_mode,
                         input_recursive=input_recursive,
                         shorten=shorten,
                         debug=debug)

    def _generate_input_files(self):
        list_file = []
        for i in self.input_files:
            if isinstance(self.input_type, str):
                if i.endswith('.' + self.input_type):
                    list_file.append(i)
            elif isinstance(self.input_type, (list, tuple)):
                for t in self.input_type:
                    if '.' + t in i:
                        list_file.append(i)
        if self.shorten:
            self.commonpath = os.path.commonpath(list_file)
        return list_file

    def row_generator(self, partitionData):
        """Returns a dict of row input to rdd spark dataframe"""
        for row in partitionData:
            path = row.path
            if self.debug:
                print(f"Convert Image {path}")  # , file=self.log_file)

            with ZipFile(self.input_path, 'r') as zipObj:
                memfile = zipObj.read(path)
                img = cv2.imdecode(np.frombuffer(memfile, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                if type(img).__name__ != "NoneType":
                    if self.resize_mode == 'padding':
                        if img.shape[0] < self.s[0]:
                            row_dict = {
                                'path': path,
                                'size': img.shape.__str__(),
                                'image': padding(img, (self.s[0], self.s[1]))
                            }
                            yield dict_to_spark_row(self.unischema, row_dict)
                        else:
                            row_dict = {
                                'path': path,
                                'size': img.shape.__str__(),
                                'image': img
                            }
                            yield dict_to_spark_row(self.unischema, row_dict)

                    elif self.resize_mode == 'resize':
                        if img.shape[0] < self.s[0]:
                            row_dict = {
                                'path': path,
                                'size': img.shape.__str__(),
                                'image': cv2.resize(img, (self.s[0], self.s[1]))
                            }
                            yield dict_to_spark_row(self.unischema, row_dict)
                        else:
                            row_dict = {
                                'path': path,
                                'size': img.shape.__str__(),
                                'image': img
                            }
                            yield dict_to_spark_row(self.unischema, row_dict)

                    else:
                        row_dict = {
                            'path': path,
                            'size': img.shape.__str__(),
                            'image': memfile
                        }
                        yield dict_to_spark_row(self.unischema, row_dict)
                else:
                    row_dict = {
                        'path': path,
                        'size': "Can not get size",
                        'image': memfile
                    }

                    yield dict_to_spark_row(self.unischema, row_dict)

    def execute(self, ROWGROUP_SIZE_MB=128):
        self.dict_image = {}

        with ZipFile(self.input_path, 'r') as zipObj:
            self.input_files = zipObj.namelist()
        logging.info(f"Total file in zip: {len(self.input_files)}")

        for s in self.size:
            self.dict_image[s] = []

        self.dict_image[self.size[0]] = self._generate_input_files()

        if self.dict_image[s]:
            self.analyze_path = self.dict_image[s]
            self.numPartition = self.get_num_partition()
            Schema = self.get_schema(s, self.image_type, self.image_color)
            self.output_path = self.convert_to_hdfs_path(self.output_path)
            output_path = self._generate_output_path(s)
            table_name = self._generate_table_name(s)
            spark = self.get_spark()

            with materialize_dataset(spark, output_path, Schema, ROWGROUP_SIZE_MB):
                self.write_to_path(spark_df=self.create_dataframe(spark=spark,
                                                                  Schema=Schema,
                                                                  input_files=self.dict_image[s],
                                                                  size=s),

                                   output_path=output_path,
                                   table_name=table_name,
                                   database=self.database,
                                   numPartition=self.numPartition,
                                   compression=self.compression)

        total_files = sum([len(self.dict_image[s]) for s in self.size])
        if total_files == 0:
            logging.warn("No files were found, check your input_path or image_type")

        logging.info("Convert complete")


class MergeFromFolderImage(ConvertFromFolderImage):
    """
    Create a parquet/delta file given local Image directory


    Parameters
    ----------
    input_path : unicode, str
        The input directory include ``png``, ``jpeg`` image
        User can add system file pattern like *

        Examples:
        input_path="/path/to/MOT17.zip"
        This pattern get all jpg in folder with different directory levels
        View https://docs.python.org/3/library/glob.html

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

    image_type : str
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

    debug : bool
        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    >>> from cads_sdk.nosql.image import ConvertFromZipImage
    >>>
    >>> converter = ConvertFromZipImage(
    >>>               input_path="/home/username/image_storage/MOT17.zip",
    >>>
    >>>               #setting output
    >>>               output_path = f"hdfs:/user/username/image/img_images_jpg.parquet",
    >>>               table_name = 'img_images_jpg',
    >>>               database = 'default',
    >>>               file_format = 'parquet', # delta|parquet
    >>>               compression = 'zstd', # |snappy|zstd
    >>>               # setting converter
    >>>               image_type = 'jpg', # |'png'|('jpg', 'png')
    >>>               image_color = 3,
    >>>               resize_mode=None, # |padding|resize
    >>>               size = [(212,212)],
    >>>
    >>>               input_recursive = True, # will loop through folder to get all pattern
    >>>              )
    >>>
    >>> converter.execute()

    Function will convert all Image in file:'/home/username/image_storage/MOT17.zip' to absolute directory hdfs:/user/username/image/img_images_jpg.parquet
    """

    def __init__(
            self,
            input_path,
            input_type,
            output_path,
            table_name='',
            database='',
            repartition=False,
            numPartition=None,
            file_format='delta',
            compression='zstd',

            image_type='jpg',
            image_color=3,
            size=[(720, 360)],
            resize_mode=None,
            input_recursive=False,

            shorten=False,
            merge_keys=['path'],

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

                         image_type=image_type,
                         image_color=image_color,
                         size=size,
                         resize_mode=resize_mode,
                         input_recursive=input_recursive,
                         shorten=shorten,
                         debug=debug)
        self.merge_keys = merge_keys

    def check_output(self, output_path):
        if not ss.exists(output_path):
            raise ValueError(f"Path {output_path} is not exists, you can only merge with exists path")

        if not check_delta(output_path):
            raise ValueError(f"Path {output_path} is not a delta table, you can only merge with delta table")

    def write_to_path(self, spark_df, output_path, table_name='', database='', numPartition=8, compression='zstd'):
        if '.parquet' in output_path.lower():
            file_format = 'delta'
        else:
            file_format = 'delta'

        spark_df.createOrReplaceTempView('new')
        # Merge new dataframe image into old dataframe

        sql_compare = ''
        for k in self.merge_keys:
            sql_compare += f"""NVL(o.{k},'') = NVL(n.{k},'')"""

        ss.sql(f"""
          MERGE INTO delta.`{output_path}` o
          USING new n ON
          {sql_compare}

          WHEN NOT MATCHED
          THEN INSERT *
        """)

        if file_format == 'delta':
            logging.info("OPTIMIZE")
            ss.sql(f"""
            OPTIMIZE delta.`{output_path}` ZORDER BY(path)
            """)

            logging.info("VACUUM")
            ss.sql(f"""
            VACUUM delta.`{output_path}` RETAIN 0 HOURS
            """)

    def execute(self, ROWGROUP_SIZE_MB=256):
        self.dict_image = {}

        for s in self.size:
            self.dict_image[s] = []

        if self.resize_mode:
            if len(self.size) == 0:
                raise ValueError("User must input size when using resize_mode")

            list_file = self._generate_input_files()

            # classify image into each size in list
            for p in list_file:
                img = cv2.imread(p)
                self.dict_image[self.check_size(img, self.size)].append(p)
        else:
            self.dict_image[self.size[0]] = self._generate_input_files()

        for s in self.size:
            if self.dict_image[s]:
                self.analyze_path = self.dict_image[s]
                self.numPartition = self.get_num_partition()
                Schema = self.create_image_schema(s, self.image_type, self.image_color)
                self.output_path = self.convert_to_hdfs_path(self.output_path)
                output_path = self._generate_output_path(s)
                self.check_output(output_path)
                table_name = self._generate_table_name(s)
                spark = self.get_spark()

                with materialize_dataset(spark, output_path, Schema, ROWGROUP_SIZE_MB):
                    self.write_to_path(spark_df=self.create_dataframe(spark=spark,
                                                                      Schema=Schema,
                                                                      input_files=self.dict_image[s],
                                                                      size=s),

                                       output_path=output_path,
                                       table_name=table_name,
                                       database=self.database,
                                       numPartition=self.numPartition,
                                       compression=self.compression)
        total_files = sum([len(self.dict_image[s]) for s in self.size])
        if total_files == 0:
            logging.warn("No files were found, check your input_path or image_type")

        logging.info("Convert complete")


class ConvertToFolderImage(ConvertToFolder):
    """
    Create a folder Image given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame


    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input (parquet) filename or dataframe include Image

        Example: df, 'file:/absolute/path/to/file.parquet'

    input_path : unicode
        Path to a local file (parquet) or hdfs file containing the Image.

        Example: df, 'file:/absolute/path/to/file.parquet'

    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a Image file (jpg, png)

        Examples:
        output_path = "/home/username/tmp"

    write_mode : str
        Default: 'recovery'
        Specify the write_mode user want to

        If write_mode = 'recovery'
        Function will convert Image to a multiple level of directory base on column path

        If write_mode != 'recovery'
        Function will convert all Image in parquet/hdfs file to one directory (output_path)

    raw_input_path : str

        Glob path that user input when use ConvertFromFolderVideo function

        For example: "/home/username/image_storage/images/**/*.jpg"

        When output it will replace '/home/username/image_storage/images/'  by ''

        That turn column path from absolute path to relative path

    keep_origin_jpg: bool | default False
        JPG is a lossly format when cv2 read jpg convert to array cv2.imread()
        And write back to jpg cv2.imwrite() it will cause 2 array 29% different
        If user want to keep origin array turn it on, but the image after convert will bigger than 400% compare with origin image

    debug : bool

        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    >>> from cads_sdk.nosql.image import ConvertToFolderImage
    >>>
    >>> converter = ConvertToFolderImage(
    >>>     input_path = '/user/username/image/img_user_device_jpg_212_212.parquet',
    >>>     raw_input_path = "/home/username/image_storage/device_images/**/*.jpg",
    >>>     output_path = '/home/username/image_storage/abc/',
    >>>     debug = False
    >>> )
    >>>
    >>> converter.execute()

    Function will convert all Image in hdfs:'/user/username/image/img_user_device_jpg_212_212.parquet' to absolute directory /home/username/image_storage/abc/
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

    def write_to_folder(self, row):
        if self.write_mode == "recovery":
            output_path = os.path.join(self.output_path, row.path.replace(self.raw_input_path, ""))
        else:
            base_path = os.path.basename(str(row.path))
            output_path = os.path.join(self.output_path, base_path)

        if self.debug:
            logging.debug("image_path: {}, row.image: {row.image}")

        self.mkdir_folder(os.path.dirname(output_path))
        with open(output_path, 'wb') as f:
            f.write(row.image)

        # if self.keep_origin_jpg:
        #     with open(output_path, 'wb') as f:
        #         f.write(row.image)
        # else:
        #     img = cv2.imdecode(np.frombuffer(row.image, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        #     # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #     cv2.imwrite(output_path, img)