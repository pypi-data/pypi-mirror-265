import cads_sdk as ss

from glob import glob
import logging
import tempfile
import os
import pandas as pd
from pathlib import Path, PurePath

from cads_sdk.nosql.utils import get_size_of_dir,get_size_of_list,check_delta,replace_special_characters


class ConvertFromFolder:
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
        # input sesssion
        self.input_path = input_path
        self.input_type = input_type
        self.input_recursive = input_recursive

        # output session
        self.output_path = output_path
        self.table_name = table_name
        self.database = database
        self.repartition = repartition
        self.numPartition = numPartition
        self.compression = compression
        self.file_format = file_format
        self.shorten = shorten

        self.debug = debug

        if debug:
            self.temp_folder = tempfile.TemporaryDirectory(dir='./tmp_sdk')
            self.tmp_file = os.path.join(self.temp_folder.name, 'sdk.log')
            self.log_file = open(self.tmp_file, 'w+')
            logging.basicConfig(level=logging.DEBUG, filename=self.tmp_file, filemode='w+')

        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

        if '.delta' in output_path:
            self.file_format = 'delta'
        else:
            self.file_format = file_format

    def _generate_input_files(self):
        if isinstance(self.input_path, str):
            list_file = self.get_all_file_in_directory()
        elif isinstance(self.input_path, (tuple, list)):
            list_file = self.input_path
        else:
            raise TypeError("Please input path string or tuple or list")
        if self.shorten:
            self.commonpath = os.path.commonpath(list_file)
        return list_file

    def get_all_file_in_directory(self):
        input_files = []
        if isinstance(self.input_type, str):
            if self.input_recursive:
                self.input_path = os.path.join(self.input_path, "**")
            self.input_path = os.path.join(self.input_path, "*." + self.input_type)
            input_files = glob(self.input_path, recursive=self.input_recursive)
            return input_files
        elif isinstance(self.input_type, (tuple, list)):
            for t in self.input_type:
                t = t.lower()
                if self.input_recursive:
                    self.input_path = os.path.join(self.input_path, "**")
                self.input_path = os.path.join(self.input_path, "*." + t)
                input_files.extend(glob(self.input_path, recursive=self.input_recursive))
            for t in self.input_type:
                t = t.upper()
                if self.input_recursive:
                    self.input_path = os.path.join(self.input_path, "**")
                self.input_path = os.path.join(self.input_path, "*." + t)
                input_files.extend(glob(self.input_path, recursive=self.input_recursive))
            return input_files

    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(
                    input_path.replace("hdfs:", ""))
            else:
                return input_path

    def _generate_output_path(self):
        if "." + self.file_format in self.output_path:
            output_path = self.output_path
        else:
            output_path = self.output_path + f".{self.file_format}"
        logging.info(f"Write at path: {output_path}")
        return output_path

    def _generate_table_name(self):
        table_name = self.table_name
        logging.info(f"Save metadata at: {table_name}")
        return table_name

    def get_num_partition(self, ROWGROUP_SIZE_MB=256):
        if self.numPartition:
            return self.numPartition
        if isinstance(self.analyze_path, str):
            memory = os.stat(self.analyze_path).st_size
        elif isinstance(self.analyze_path, (tuple, list)):
            memory = get_size_of_list(self.analyze_path)
        else:
            memory = 0
        logging.info(f"Total folder memory: {memory}")
        numPartition = int(round(memory / 1024 / 1024 / ROWGROUP_SIZE_MB))
        if numPartition <= 8:
            return None
        else:
            return numPartition

    def coalesce_dataframe(self, spark_df, numPartition):
        if self.file_format != 'delta':
            numPartition = self.get_num_partition()
            if numPartition:
                if numPartition > 8:
                    return spark_df.repartition(numPartition)
                else:
                    return spark_df.coalesce(numPartition)
        return spark_df

    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark

    def create_dataframe(self,
                         spark,
                         Schema,
                         input_files):
        from pyspark.sql.functions import expr
        self.unischema = Schema
        spark_df = spark.createDataFrame(pd.DataFrame(input_files, columns=['path']))
        if self.shorten:
            return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator),
                                         Schema.as_spark_schema()).withColumn("rel_path", expr(
                f"""replace(path, '{self.commonpath}', '') """))
        else:
            return spark.createDataFrame(spark_df.rdd.mapPartitions(self.row_generator), Schema.as_spark_schema())

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
            if self.shorten:
                logging.info("OPTIMIZE")
                ss.sql(f"""
                OPTIMIZE delta.`{output_path}` ZORDER BY(rel_path)
                """)
            logging.info("VACUUM")
            ss.sql(f"""
            VACUUM delta.`{output_path}` RETAIN 0 HOURS
            """)


class ConvertToFolder:
    def __init__(
        self,
        data = None,
        input_path:str=None,
        output_path:str='./output',
        write_mode = "recovery",
        raw_input_path = "",
        debug = False
    ):

        from pyspark.sql.dataframe import DataFrame

        if debug:
            logging.basicConfig(level=logging.DEBUG, filename='sdk.log', filemode='w')
        else:
            logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

        check_parent_path = raw_input_path.split('*')
        if len(check_parent_path) > 1:
            raw_input_path = check_parent_path[0]

        if isinstance(data, (Path, PurePath)):
            input_path = str(data)
            data = None
        elif data is not None and isinstance(data, str):
            if ss.exists(data):
                input_path = data
                data = None
        elif isinstance(data, DataFrame):
            self.input_path = input_path
            self.output_path = output_path
            self.write_mode = write_mode
            self.raw_input_path = raw_input_path
            self.data = data

            self.debug = debug

            write_to_folder = self.__init__(write_mode=write_mode, raw_input_path=raw_input_path, output_path=output_path, debug=debug).write_to_folder
            self.write_abtract = write_to_folder #data.foreach(write_to_folder)

        self.input_path = input_path
        self.output_path = output_path
        self.write_mode = write_mode
        self.raw_input_path = raw_input_path
        self.data = data

        self.debug = debug

    def get_spark(self):
        return ss.PySpark(driver_memory='32G', num_executors='8', executor_memory='4G', port='', yarn=False).spark

    def convert_to_hdfs_path(self, input_path):
        if "file:" in input_path:
            return input_path
        else:
            if "hdfs://hdfs-cluster.datalake.bigdata.local:8020" not in os.path.dirname(input_path):
                return "hdfs://hdfs-cluster.datalake.bigdata.local:8020" + os.path.abspath(
                    self.input_path.replace("hdfs:", ""))
            else:
                return input_path

    def mkdir_folder(self, output_path):
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    def write_to_folder(self, row):
        """
        Need to modify function
        """
        pass

    def execute(self):
        self.mkdir_folder(os.path.dirname(self.output_path))
        spark = self.get_spark()
        if self.data:
            self.data.foreach(self.write_abtract)
        else:
            if check_delta(self.input_path):
                logging.info("Detect Delta File")
                df = ss.sql(f"""select * from delta.`{self.input_path}`""")
            else:
                df = ss.sql(f"""select * from parquet.`{self.input_path}`""")
            df.foreach(self.write_to_folder)
        logging.info("Convert complete")
