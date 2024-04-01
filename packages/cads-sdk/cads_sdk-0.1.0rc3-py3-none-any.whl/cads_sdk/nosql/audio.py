# ---------------------------------#
# ------- AUDIO SESSION -----------#
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

from cads_sdk.utils import import_or_install
import_or_install("pydub")
import pydub

import_or_install("scipy")
from scipy.io import wavfile

from petastorm.etl.dataset_metadata import materialize_dataset

from cads_sdk.nosql.codec import *
from cads_sdk.nosql.utils import get_size_of_dir,get_size_of_list,check_delta,replace_special_characters
from cads_sdk.nosql.base import ConvertFromFolder, ConvertToFolder


class ConvertFromFolderAudio(ConvertFromFolder):
    """
    Create a parquet/delta file given local Image directory


    Parameters
    ----------
    input_path : unicode, str
        The input filename include ``mp3``, ``waw``, ``pcm``
        User can add system file pattern like *

        Examples:
        input_path="./"
        input_path="/home/username/path/"

    input_type : unicode, str
        Examples: 'mp3'

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


    input_recursive : bool
        Default: True

        If True:
        will loop through folder to get all pattern

    debug : bool

        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    >>> from cads_sdk.nosql.audio import ConvertFromFolderAudio
    >>> # Test case 1, write with mp3 audio:
    >>> converter = ConvertFromFolderAudio(
    >>>               input_path='./audio_mp3/*.mp3',
    >>>               input_recursive = False,
    >>>               output_path = f"file:/home/username/image_storage/audio_mp3.parquet",
    >>>              )
    >>> converter.execute()

    >>> # Test case 2, write with PCM audio:
    >>> converter = ConvertFromFolderAudio(
    >>>               input_path='./audio_pcm/*.pcm',
    >>>               input_recursive = False,
    >>>               output_path = f"file:/home/username/image_storage/audio_pcm.parquet",
    >>>              )
    >>>
    >>> converter.execute()

    >>> # Test case 3, write with Wav audio:
    >>> converter = ConvertFromFolderAudio(
    >>>               input_path='./audio_wav/*.wav',
    >>>               input_recursive = False,
    >>>               output_path = f"file:/home/username/image_storage/audio_wav.parquet",
    >>>              )
    >>>
    >>> converter.execute()
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
                         input_recursive=input_recursive,
                         shorten=shorten,
                         debug=debug)

    def guess_type(self, input_path):
        dict_type = {
            'wav': np.float64,
            'pcm': np.float64,
            'mp3': np.int16,
            'mp4': np.bytes_,
            'jpg': np.uint8,
            'png': np.uint8
        }

        for t in dict_type.keys():
            if "." + t in input_path:
                return t

    def numpy_map_type(self, input_files):
        dict_type = {
            'wav': np.bytes_,
            'pcm': np.bytes_,
            'mp3': np.bytes_,
            'mp4': np.bytes_,
            'jpg': np.uint8,
            'png': np.uint8
        }

        if input_files:
            return dict_type[self.guess_type(input_files[0])]
        else:
            raise "Please check cho input_path, there is no file {input_files}"

    def row_generator(self, partitionData):
        """Returns a single entry in the generated dataset. Return a bunch of random values as an example."""
        for row in partitionData:
            path = row.path
            if self.debug:
                logging.debug(f"Convert audio {path}")

            if self.guess_type(path) == 'pcm':
                samplerate, data = read_pcm(path)
                channels = 1

                data = data.tobytes()

            elif self.guess_type(path) == 'wav':
                samplerate, data = wavfile.read(path)
                if len(data.shape) == 2:
                    channels = 2
                else:
                    channels = 1

                with open(path, 'rb') as file:
                    data = file.read()

            if self.guess_type(path) == 'pcm':
                samplerate, data = read_pcm(path)
                channels = 1

            elif self.guess_type(path) == 'mp3':
                samplerate, data = read_mp3(path)
                if len(data.shape) == 2:
                    data = data.T
                    channels = 2
                else:
                    channels = 1

                with open(path, 'rb') as file:
                    data = file.read()

            row_dict = {'path': path,
                        'samplerate': samplerate,
                        'channels': channels,
                        'audio': data}

            yield dict_to_spark_row(self.unischema, row_dict)

    def get_schema(self):
        return Unischema('Audio', [
            UnischemaField('path', np.str_, (), ScalarCodec(StringType()), False),
            UnischemaField('samplerate', np.int_, (), ScalarCodec(IntegerType()), False),
            UnischemaField('channels', np.int_, (), ScalarCodec(IntegerType()), False),
            UnischemaField('audio', self.numpy_map_type(self.analyze_path), (1000,),
                           AudioCodec(self.guess_type(self.analyze_path[0])), False)
        ])

    def execute(self, ROWGROUP_SIZE_MB=256):
        input_files = self._generate_input_files()
        self.analyze_path = input_files
        self.numPartition = self.get_num_partition()
        self.output_path = self.convert_to_hdfs_path(self.output_path)
        output_path = self._generate_output_path()
        table_name = self._generate_table_name()
        Schema = self.get_schema()
        spark = self.get_spark()

        if input_files:
            self.write_to_path(spark_df=self.create_dataframe(
                spark=spark,
                Schema=Schema,
                input_files=input_files
            ),
                output_path=output_path,
                table_name=table_name,
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


class MergeFromFolderAudio(ConvertFromFolderAudio):
    """
    Create a parquet/delta file given local Image directory


    Parameters
    ----------
    input_path : unicode, str
        The input directory include ``mp3``, ``pcm``, ``wav`` file
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


    debug : bool

        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    >>> from cads_sdk.nosql.audio import MergeFromFolderAudio
    >>>
    >>> converter = ConvertFromFolderAudio(
    >>>               input_path='./audio_wav/*.wav',
    >>>               input_recursive = False,
    >>>               output_path = f"file:/home/username/image_storage/audio_wav.delta",
    >>>              )
    >>>
    >>> converter.execute()
    Function will convert all Audio in file:'./audio_wav/*.wav' to absolute directory "file:/home/username/image_storage/audio_wav.delta"
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

            shorten=False,
            merge_keys=['path'],
            input_recursive=False,

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
        input_files = self._generate_input_files()
        self.analyze_path = input_files
        self.numPartition = self.get_num_partition()
        self.output_path = self.convert_to_hdfs_path(self.output_path)
        output_path = self._generate_output_path()
        table_name = self._generate_table_name()
        Schema = self.get_schema()
        spark = self.get_spark()

        if input_files:
            self.write_to_path(spark_df=self.create_dataframe(spark=spark,
                                                              Schema=Schema,
                                                              input_files=input_files),

                               output_path=output_path,
                               table_name=table_name,
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


class ConvertToFolderAudio(ConvertToFolder):
    """
    Create a folder Audio given hdfs_path/local_path or pyspark.sql.dataframe.DataFrame


    Parameters
    ----------
    data : unicode, str or pyspark.sql.dataframe.DataFrame
        The input filename to load Audio or dataframe include Audio

    input_path : unicode
        Path to a local file or hdfs file containing the audio.

    output_path : unicode
        Path to a local file that function execute() will convert parquet/delta back to a video file (pcm, mp3, wav...)

    write_mode : str
        Specify the write_mode user want to

        If write_mode = 'recovery'
        Function will convert audio to a multiple level of directory base on column path

        If write_mode != 'recovery'
        Function will convert all audio in parquet/hdfs file to one directory (output_path)

    raw_input_path : str
        Glob path that user input when use ConvertToFolderAudio function
        For example: "/home/username/image_storage/audio_mp3/*.mp3"

        When output it will replace '/home/username/image_storage/audio_mp3/'  by ''
        That turn column path from absolute path to relative path

    debug : bool

        If debug=True:
        Write log into sdk.log file and print more debug information


    Examples
    --------
    >>> from cads_sdk.nosql.audio import ConvertToFolderAudio
    >>> converter = ConvertToFolderAudio(
    >>> input_path = 'file:/home/username/image_storage/audio_mp3.parquet',
    >>> raw_input_path = '/home/username/image_storage/audio_mp3/*.mp3',
    >>> output_path = './abc',
    >>> write_mode = "recovery"
    >>> )
    >>>
    >>> converter.execute()

    Function will convert all audio in file:/home/username/image_storage/audio_mp3.parquet to relative directory abc
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
            wfile.write(row.audio)