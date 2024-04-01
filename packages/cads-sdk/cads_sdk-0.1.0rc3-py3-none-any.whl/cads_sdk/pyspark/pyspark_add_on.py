import os
import findspark

from cads_sdk.utils import get_today
findspark.init(os.getenv("SPARK_HOME"))

import sys
import pandas as pd
from pyspark.sql.utils import AnalysisException

from cads_sdk.pyarrow.pyarrow_add_on import PyArrow
from cads_sdk.pyspark.cache import MemoryCacheToken
from cads_sdk.pyspark.writter_options import DataFrameWriter
from cads_sdk.utils import log, query_yes_no
import logging


if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


class Utf8Encoder(object):
    def __init__(self, fp):
        self.fp = fp

    def write(self, data):
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        self.fp.write(data)


# display options
try:
    import IPython
    IPython.auto_scroll_threshold = 100000

    from IPython.core.interactiveshell import InteractiveShell
    InteractiveShell.ast_node_interactivity = "all"
    from IPython.display import display

    from IPython.core.display import HTML
    display(HTML("<style>pre { white-space: pre !important; }</style>"))

except Exception as e:
    log("IPython", e)

pd.options.display.max_columns = 50
VAULT_ROLE_ID = None
VAULT_SECRET_ID = None


class PySpark:
    def __init__(self, driver_memory='1G', num_executors='1', executor_memory='4G', port='', yarn=False, **spark_configs):
        """
         Parameters
        ----------

        driver_memory: memory for spark driver and executor memory, must less than 8Gb. 8Gb is handle table 10 milion rows
        executor_memory: memeory for core spark, must less than 8G
        core: executor core, must less than 10 cores
        port: change port if user false job
        yarn: (boolan) if True is run with yarn mode, if False run with local mode
        spark_configs: add more extensions by add_on1 = ("spark.dynamicAllocation.enabled", "true")
        """
        global spark, memory_cache_token

        self.driver_memory = driver_memory
        self.executor_memory = executor_memory
        self.num_executors = num_executors
        self.port = port

        if yarn:
            self.yarn = 'yarn'
        else:
            self.yarn = f'local[{self.num_executors}]'

        # create spark session
        from pyspark import SparkConf
        from pyspark.sql import SparkSession

        conf = SparkConf()

        # config spark application name
        import getpass
        conf.setAppName(f"spark_sdk_{getpass.getuser()}")

        # config location for spark finding metadata from hive metadata server
        # from cads_sdk.conf import (HIVE_IP_NODES1, HIVE_IP_NODES2)
        # conf.set("hive.metastore.uris", HIVE_IP_NODES1+","+HIVE_IP_NODES2)

        # config in-memory columnar data format that is used in Spark to efficiently transfer data between JVM and Python processes
        conf.set("spark.kryoserializer.buffer.max", "2000")
        conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
        # conf.set("spark.sql.execution.arrow.enabled", "true") # remove in future
        conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "10000")

        if self.yarn == 'yarn':
            #queue
            conf.set("spark.yarn.queue", "batch")

            # config spark dynamicAllocation
            conf.set("spark.dynamicAllocation.enabled", "true")
            conf.set("spark.dynamicAllocation.shuffleTracking.enabled", "true")
            conf.set("spark.dynamicAllocation.minExecutors", 1)
            conf.set("spark.dynamicAllocation.maxExecutors", 8)
            conf.set("spark.dynamicAllocation.executorIdleTimeout", "300s")
            conf.set("spark.dynamicAllocation.shuffleTracking.enabled", "true")
            conf.set("spark.dynamicAllocation.shuffleTracking.timeout", "300s")
        else:
            # config directory to use for "scratch" space in Spark, including map output files and RDDs that get stored on disk
            conf.set('spark.local.dir', '/tmp')

        # config partition Size
        # conf.set('spark.sql.adaptive.coalescePartitions.minPartitionSize', '128MB')
        conf.set('spark.sql.files.minPartitionNum', 100000)

        # config spark driver memory
        conf.set("spark.driver.memory", self.driver_memory)
        conf.set('spark.executor.memory', self.executor_memory)
        conf.set('spark.driver.maxResultSize', '10G')

        if int(self.num_executors) > 1:
            conf.set('spark.num.executors', int(self.num_executors))
            conf.set('spark.executor.cores', 5)
        conf.set('spark.rpc.message.maxSize', '1000')

        # conf.set("spark.ui.enabled", "false")
        if not port:
            port = 0
            for j,i in enumerate(getpass.getuser()):
                port+=ord(i) * 1 if j//2 == 1 else -1
            port +=4300
        conf.set("spark.ui.port", port)
        conf.set("spark.port.maxRetries", "50")

        # config for write append parquet
        conf.set("spark.sql.parquet.compression.codec", "snappy")

        # set metastore.client.capability.check to false
        conf.set("hive.metastore.client.capability.check", "false")

        # config for descrypt data
        from cads_sdk.conf import LIST_JARS
        if LIST_JARS:
            conf.set("spark.jars", LIST_JARS)

        # conf.set("spark.jars", "hdfs:///shared/jars/hotpot_2.12-0.0.3.jar")
        conf.set("spark.sql.redaction.string.regex", ".{22}==")

        # delta format
        if LIST_JARS:
            if 'delta_delta' in LIST_JARS:
                conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
                conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
                conf.set("spark.sql.catalogImplementation","hive")
                conf.set('spark.sql.hive.metastorePartitionPruningFallbackOnException', True)
                conf.set('spark.sql.hive.metastorePartitionPruningFastFallback', True)
                conf.set("spark.databricks.delta.optimize.maxFileSize", 268435456) # 256MB
                conf.set('spark.databricks.delta.retentionDurationCheck.enabled', False)
        # conf.set('spark.jars.packages', "io.delta:delta-core_2.12:2.1.0")
        # conf.set("spark.driver.extraJavaOptions", "-Dhttps.proxyHost=proxy.hcm.fpt.vn -Dhttps.proxyPort=80 -Dhttp.proxyHost=proxy.hcm.fpt.vn -Dhttp.proxyPort=80")
        # conf.set("spark.executor.extraJavaOptions", "-Dhttps.proxyHost=proxy.hcm.fpt.vn -Dhttps.proxyPort=80 -Dhttp.proxyHost=proxy.hcm.fpt.vn -Dhttp.proxyPort=80")

        if LIST_JARS: #
            if 'iceberg_iceberg' in LIST_JARS: # prioritize iceberg
                conf.set("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
                conf.set("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")
                conf.set("spark.sql.catalogImplementation", "hive")

        # fix legacy parquet timestamp error
        conf.set("spark.sql.parquet.int96RebaseModeInRead", "CORRECTED")
        conf.set("spark.sql.parquet.int96RebaseModeInWrite", "CORRECTED")
        conf.set("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED")
        conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED")

        # lineage
        from cads_sdk.conf import GMS_URL_KEY, GMS_AUTH_TOKEN, LIST_JARS
        if LIST_JARS:
            if "datahub-spark-lineage" in LIST_JARS:
                conf.set("spark.extraListeners", "datahub.spark.DatahubSparkListener")
                conf.set("spark.datahub.rest.server", GMS_URL_KEY)
                conf.set("spark.datahub.rest.token", GMS_AUTH_TOKEN)

        # config for parquet-encryption
        conf.set("spark.hadoop.parquet.encryption.plaintext.footer", "true")
        conf.set("spark.hadoop.parquet.encryption.kms.client.class", "org.apache.parquet.crypto.keytools.cads.VaultClient")
        conf.set("spark.hadoop.parquet.crypto.factory.class", "org.apache.parquet.crypto.keytools.PropertiesDrivenCryptoFactory")
        conf.set("spark.hadoop.parquet.encryption.kms.instance.url", "https://demo-vault.cads.live")

        # add other spark config
        self.add_spark_configs(conf, spark_configs)

        # kerberos
        # if os.path.exists("/tmp/krb5cc_1000"):
            # conf.set("spark.kerberos.keytab", "/tmp/krb5cc_1000")
        # else:
            # log("Kerberos", "You need to login kerberos before start spark if not use cannot access to datalake")

        session = SparkSession._instantiatedSession
        if session is None or session._sc._jsc is None:
            spark = SparkSession.builder.config(conf=conf).master(self.yarn).enableHiveSupport().getOrCreate()
            self.spark = spark
            logging.debug("Create new spark")
            all_config = {c[0]: c[1] for c in self.spark.sparkContext.getConf().getAll()}
            memory_cache_token = MemoryCacheToken(all_config)
        else:
            self.spark = SparkSession.builder.config(conf=conf).master(self.yarn).enableHiveSupport().getOrCreate()
        # config timezone
        self.spark.conf.set('spark.sql.session.timeZone', '+07:00')

        # config show pandas dataframe format on notebook
        self.spark.conf.set("spark.sql.repl.eagerEval.enabled", True)
        self.spark.conf.set("spark.sql.repl.eagerEval.truncate", 200)

        # self.spark.conf.get("hive.metastore.uris")

        # defing decrypt function
        try:
            self.spark._jvm.vn.fpt.insights.utils.Helper.registerUdf("fdecrypt", "fdecrypt")
            self.spark._jvm.vn.fpt.insights.utils.Helper.registerUdf("fencrypt", "fencrypt")
            self.spark._jvm.vn.fpt.insights.utils.Helper.registerUdf("fmask", "fmask")
        except:
            pass

        # dont print WARN
        self.spark.sparkContext.setLogLevel("ERROR")

        if 'memory_cache_token' in globals():
            vault_token = memory_cache_token.cache_token()
            if vault_token:
                self.spark.conf.set("spark.hadoop.parquet.encryption.key.access.token", vault_token)
        else:
            log("Parquet Encryption", "You are not login, you cannot encrypt or decrypt columns")

    def add_spark_configs(self, conf, spark_configs):
        all_config = {c[0]:c[1] for c in conf.getAll()}
        for k_c in spark_configs.keys():
            if len(spark_configs[k_c]) == 2:
                if spark_configs[k_c][0] in ['spark.repl.local.jars', 'spark.sql.hive.metastore.jars', 'spark.jars']:
                    conf.set(spark_configs[k_c][0], all_config[spark_configs[k_c][0]]+','+spark_configs[k_c][1])
                elif spark_configs[k_c][0] == 'VAULT_ROLE_ID':
                    logging.debug("VAULT_ROLE_ID: "+spark_configs[k_c][1])
                    conf.set("spark.hadoop.parquet.encryption.kms.instance.id", spark_configs[k_c][1])
                elif spark_configs[k_c][0] == 'VAULT_SECRET_ID':
                    logging.debug("VAULT_SECRET_ID: "+spark_configs[k_c][1])
                    conf.set("spark.hadoop.parquet.encryption.kms.instance.password", spark_configs[k_c][1])
                else:
                    conf.set(spark_configs[k_c][0], spark_configs[k_c][1])
            else:
                raise TypeError(f"PySpark got an unexpected keyword argument {k_c}")

    def get_fs(self):
        # get hadoop file system
        return self.spark._jvm.org.apache.hadoop.fs.FileSystem.get(self.spark._jsc.hadoopConfiguration())

    def check_is_file(self, hdfs_path):
        fs = self.get_fs()
        return fs.exists(self.spark._jvm.org.apache.hadoop.fs.Path(hdfs_path))

    def check_empty(self, hdfs_path):
        from cads_sdk import pyarrow as pa
        list_path = pa.ls(hdfs_path)
        if len(list_path) > 0:
            return False
        else:
            return True

    def _to_java_object_rdd(self, rdd):
        from pyspark.serializers import PickleSerializer, AutoBatchedSerializer
        """ Return a JavaRDD of Object by unpickling
        It will convert each Python object into Java object by Pyrolite, whenever the
        RDD is serialized in batch or not.
        """
        rdd = rdd._reserialize(AutoBatchedSerializer(PickleSerializer()))
        JavaObj = rdd.ctx._jvm.org.apache.spark.mllib.api.python.SerDe.pythonToJava(rdd._jrdd, True)

        return JavaObj

    def convert_size(self, size_bytes):
        """
        return at MB
        """
        return size_bytes / 1024 / 1024

    def num_repartition(self, sparkDF):
        """
        Number Partition
        If file < 128MB ==> num_partition = 1
        If file between 128MB and 256MB ==> num_partition = 2
        """
        memory_byte = self.spark._jvm.org.apache.spark.util.SizeEstimator.estimate(
            self._to_java_object_rdd(sparkDF.rdd))

        memory_mb = self.convert_size(memory_byte)

        return int(memory_mb // (128 * 300) + 1)

    def check_keys_path_format(self, keys_path):
        import re
        if re.search('json$', keys_path):
            return True
        else:
            raise Exception("keys_path must end with '.json'")

    def autogenerate_key(self, length_key=22):
        """
        Input length of string key
        return random string (contains string upper case and string lower case) and digits
        """
        import string
        import random

        key = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length_key))
        key = key + "=="
        return key

    def auto_generate_list_keys(self, table_name, column_name='', keys_path='keys.json'):
        """
        Input
        table_name: Name of table that need encrypt
        column_name: list string seperate by ',', ex: a,b,c
        keys_path: path file of key if want to append key to file

        return list of keys ready to be copy
        """
        from datetime import datetime

        if self.check_is_file(keys_path):
            list_keys = PyArrow().read_json(keys_path)
        else:
            list_keys = []

        for c in column_name.split(','):
            if c:
                keys = {}

                keys["name"] = f"secret_for_{table_name}_{c}"
                keys["description"] = f"This is secret_for_{table_name}_{c}"
                keys["created"] = round(datetime.timestamp(datetime.now()))
                keys["material"] = self.autogenerate_key()

                list_keys.append(keys)
        return list_keys

    def encrypt_column(self, sparkDF, table_name, column_names=[], keys_path=''):
        """
        Input
        : sparkDF: spark.sql.DataFrame
        : table_name: name of table example: table1
        : column_names: list column name need encrypt
        : keys_path: json path example: /path/to/keys.json
        return: spark.sql.DataFrame have encrypted column
        """
        # check file keys exist
        if self.check_is_file(keys_path):
            # Opening JSON file
            list_keys = PyArrow().read_json(keys_path)
        else:
            list_keys = []

        keys_exist = {}
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            # check if key in file
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]

        for c in column_names:
            # if not found key generate new key append to keys.json
            if c not in keys_exist.keys():
                log('Append key for', c)
                PyArrow().append_keys_to_file(table_name, c, keys_path)

        list_keys = PyArrow().read_json(keys_path)
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]

        fields = "\n                "
        comma = ",\n                "

        for s in sparkDF.schema:
            c = s.name
            if c in column_names:
                field_dev = f"""fencrypt({c}, '{keys_exist[c]}') as {c}{comma}"""
            else:
                field_dev = f"{c}{comma}"

            fields += field_dev

        fields = fields[:-len(comma)]

        sql = f"""
        SELECT 
            {fields}
        FROM {table_name}
        """

        sparkDF.createOrReplaceTempView(f"{table_name}")
        log("encrypt_column", "Start encrypt column")

        return self.spark.sql(sql)

    def read_first_file(self, database, table_name, hdfs_path):
        '''
        Read schema hive
        '''
        try:
            df = self.spark.sql(f"""SELECT * FROM {database}.{table_name} LIMIT 5""")
        except:
            if 'parquet' in hdfs_path:
                df = self.spark.sql(f"""SELECT * FROM parquet.`{hdfs_path}` LIMIT 5""")
            else:
                raise AnalysisException(f"Table or view not found {database}.{table_name}")
        return df

    def compare_data_type(self, first_sparkDF, second_sparkDF):
        """
        Function to check when write data second time
        """
        def get_data_type(datatype):
            mapping = {'LongType()': 'IntegerType()', 'IntegerType()': 'LongType()'}
            if datatype in mapping.keys():
                return mapping[datatype]
            else:
                return datatype

        error = {}
        if len(first_sparkDF.schema) == len(second_sparkDF.schema):
            for c in second_sparkDF.schema:
                c_name = c.name
                second_type = second_sparkDF.schema[c_name].dataType
                second_type = str(second_type)
                first_type = first_sparkDF.schema[c_name].dataType
                first_type = str(first_type)

                if first_type != second_type:
                    if first_type != get_data_type(second_type):
                        error[c_name] = {'first_time': first_type, 'second_time': second_type}

                if error.keys():
                    log('Error', error)
                    first_sparkDF.unpersist()
                    second_sparkDF.unpersist()
                    raise TypeError(f"DataType of Columns this time store is not like first time {error}")
        else:
            print(f'First time have columns', first_sparkDF.schema.names)
            print(f'Second time have columns', second_sparkDF.schema.names)

            raise ValueError(f"First time have {len(first_sparkDF.schema)} columns but second time have {len(second_sparkDF.schema)} columns")



        log("compare_data_type", "Check schema OK")
        first_sparkDF.unpersist()

    def refresh_table(self, database, table_name, partition_by=''):
        if partition_by:
            log("refresh_table", "MSCK REPAIR DATA FOR PARTITION TABLE")
            self.spark.sql(f'msck REPAIR TABLE {database}.{table_name}')

        self.spark.sql(f"""REFRESH TABLE {database}.{table_name}""")

    def create_table_and_metadata(self, database, table_name, hdfs_path, partition_by=''):
        """
        Create table in catalog and MSCK (update metadata) if partitioned table
        Input:
        :param database: database name, example: default
        :param table_name: table name, example: test1
        :param hdfs_path: path to data, example /path/to/data.parquet
        Return:
        nothing
        """
        if database and table_name:
            try:
                self.spark.catalog.createTable(database + '.' + table_name, "hdfs://" + hdfs_path)
            except:
                # AnalysisException table aready exists
                log("create_table_and_metadata", "Cannot create table, this table already exists ==> repair data")

        elif database and not table_name:
            raise Exception("You must add parameters table_name=")

        elif not database and table_name:
            raise Exception("You must add database=")

        self.refresh_table(database=database, table_name=table_name, partition_by=partition_by)

    def verify_hdfs_path(self, hdfs_path):
        if hdfs_path:
            import re
            pattern = re.compile('^hdfs://')
            is_hdfs = pattern.search(hdfs_path)
            if not is_hdfs and 'file:' not in hdfs_path:
                hdfs_path = 'hdfs://' + hdfs_path

        return hdfs_path

    def create_table_if_not_exists(self, database, table_name, file_format, partition_by, sparkDF):
        sql = f"CREATE TABLE IF NOT EXISTS {database}.{table_name} USING {file_format}"
        if partition_by:
            sql += " "
            sql += f"PARTITIONED BY({partition_by})"
        sparkDF.createOrReplaceTempView("sparkDF")
        sql += " AS SELECT * FROM sparkDF"
        self.spark.sql(sql)

    def store_spark_dataframe_to_dwh(self, data, hdfs_path="", repartition=False, numPartitions=None, partition_by='',
                                     partition_date='', file_format='iceberg', compression='snappy',
                                     database='', table_name='', encrypt_columns:list=None, keys_path=''):
        """
         Parameters
        ----------
        data: pyspark.sql.dataframe.DataFrame
        hdfs_path : Path hdfs user want to store. EX: /data/fpt/ftel/cads/opt_customer/dm/

        partition_by: columns user want to partition, if None do not partition
        database : If user want to store to database must have database
        table_name: If user want to map data hdfs to table must have table_name
        """
        from pyspark.sql.functions import to_date, lit
        if not file_format:
            if '.delta' in hdfs_path.lower():
                file_format = 'delta'
            elif '.ice' in hdfs_path.lower():
                file_format = 'iceberg'
            elif '.parquet' in hdfs_path.lower():
                file_format = 'parquet'
            else:
                file_format = 'iceberg'

        hdfs_path = self.verify_hdfs_path(hdfs_path)
        options = {}
        if hdfs_path:
            options["path"] = hdfs_path
        options["compression"] = compression

        sparkDF = data

        # new encrypt
        encrypt_columns_config = []
        if encrypt_columns:
            for c in encrypt_columns:
                encrypt_columns_config.append(database + "__" + table_name + "__" + c + ":" + c)
            encrypt_footer_config = database + "__" + table_name
            options["parquet.encryption.column.keys"] = ",".join(encrypt_columns_config)
            options["parquet.encryption.footer.key"] = encrypt_footer_config

        # old method
        # if encrypt_columns:
        #     if keys_path:
        #         if self.check_keys_path_format(keys_path):
        #             sparkDF = self.encrypt_column(sparkDF=sparkDF, table_name=table_name, column_names=encrypt_columns,
        #                                           keys_path=keys_path)
        #     else:
        #         raise Exception("You must add parameters keys_path=")


        if partition_by:
            if partition_by in data.columns:
                import pyspark.sql.functions as F
                from pyspark.sql.functions import col
                check_date = sparkDF.select(F.length(col(partition_by))).distinct().collect()
                if check_date:
                    if 10 in list(check_date[0]):
                        sparkDF = sparkDF.withColumn(partition_by, to_date(partition_by))
            else:
                if not partition_date:
                    query_yes_no("""You should config partition_date, default today \nContinues Y/n?""")
                    partition_date = get_today()

                # add constant column string ELT_DATE
                sparkDF = sparkDF.withColumn(partition_by, lit(partition_date))
                # convert string to date
                sparkDF = sparkDF.withColumn(partition_by, to_date(partition_by))

            log("HDFS path: ", hdfs_path)

            # if table exist compare datatype before store
            if hdfs_path:
                if self.check_is_file(hdfs_path):
                    if not self.check_empty(hdfs_path):
                        self.compare_data_type(self.read_first_file(database, table_name, hdfs_path), sparkDF)

            self.create_table_if_not_exists(database=database, table_name=table_name,
                                            file_format=file_format, partition_by=partition_by,
                                            sparkDF=sparkDF)
            self.spark.sql("SET spark.sql.sources.partitionOverwriteMode = dynamic")

            # sparkDF.repartition(numPartitions).write.format(file_format).option('compression', compression).mode("overwrite").partitionBy(partition_by).option("path", hdfs_path).saveAsTable(database + '.' + table_name)
            if repartition:
                numPartitions = partition_by

                sparkDF.repartition(numPartitions) \
                    .write.format(file_format) \
                    .mode("overwrite") \
                    .partitionBy(partition_by) \
                    .sdk_options(options) \
                    .saveAsTable(database + '.' + table_name)
            else:
                sparkDF\
                    .write.format(file_format) \
                    .mode("overwrite") \
                    .partitionBy(partition_by) \
                    .sdk_options(options) \
                    .saveAsTable(database + '.' + table_name)

        else:
            if repartition:
                if not numPartitions:
                    numPartitions = self.num_repartition(sparkDF)
                sparkDF.repartition(numPartitions) \
                    .write.format(file_format) \
                    .mode("overwrite") \
                    .sdk_options(options) \
                    .saveAsTable(database + '.' + table_name)
            else:
                sparkDF \
                    .write.format(file_format) \
                    .mode("overwrite") \
                    .sdk_options(options) \
                    .saveAsTable(database + '.' + table_name)

        self.spark.sql(f"""REFRESH TABLE {database}.{table_name}""")

        try:
            from cads_sdk.pyspark.pylineage import addLineageAfterToDwh
            addLineageAfterToDwh(database+'.'+table_name)
        except Exception as e:
            log("pylinage", e)
            pass

    def to_dwh_spark(self, data, hdfs_path, repartition=False, numPartitions=None, partition_by='', partition_date='',
                     compression='snappy', file_format='iceberg',
                     database='', table_name='', encrypt_columns=[], keys_path=''):
        """
        Parameters
        ----------
        file_format
        keys_path
        encrypt_columns
        compression
        partition_date
        numPartitions
        repartition
        data: pandas dataframe
        hdfs_path : Path hdfs user want to store. EX: /data/fpt/ftel/cads/opt_customer/dm/
        partition_by: columns user want to partition, if None do not partition
        database : If user want to store to database must have database
        table_name: If user want to map data hdfs to table must have table_name
        """
        sparkDF = self.spark.createDataFrame(data)
        self.store_spark_dataframe_to_dwh(sparkDF, hdfs_path=hdfs_path, repartition=repartition,
                                          numPartitions=numPartitions, partition_by=partition_by,
                                          partition_date=partition_date, database=database, table_name=table_name,
                                          encrypt_columns=encrypt_columns, keys_path=keys_path,
                                          compression=compression, file_format=file_format)

    def project_table(self, table, row_filter, limit):
        sql = "SELECT * FROM "
        if table.name():
            full_table_name = convert_table_name_to_spark_name(table.name())
            sql += full_table_name

            # if row_filter:
            if limit:
                sql += f"limit {limit}"
            return self.spark.sql(sql)

    def read_csv(self, path, sep=',', header=True):
        return self.spark.read.option("header",header).options(delimiter=sep).csv(path)

    def read_parquet(self, path):
        return self.spark.read.parquet(path)

    def describe_table(self, full_table_name, to_pandas=False):
        if to_pandas:
            pd.set_option('max_colwidth', 300)
            return self.spark.sql(f"""DESCRIBE FORMATTED {full_table_name}""").toPandas()
        else:
            return self.spark.sql(f"""DESCRIBE FORMATTED {full_table_name}""").show(100, 200)

    def show_table(self, database, to_pandas=False):
        if to_pandas:
            pd.set_option('max_colwidth', 300)
            return self.spark.sql(f"""SHOW TABLES FROM {database}""").toPandas()
        else:
            return self.spark.sql(f"""SHOW TABLES FROM {database}""").show(100, 200)

    def stop(self):
        self.spark.stop()
        return True


def convert_table_name_to_spark_name(name_list: list):
    if len(name_list) == 3:
        return name_list[1] + "." + name_list[2]


