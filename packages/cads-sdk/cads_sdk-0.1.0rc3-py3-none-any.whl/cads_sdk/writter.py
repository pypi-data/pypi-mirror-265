from cads_sdk.pyspark.pyspark_add_on import PySpark
from cads_sdk.pyarrow.pyarrow_add_on import PyArrow, PyArrowWritter

from cads_sdk.add_on import get_spark, refresh_table_metadata
from cads_sdk.utils import choose_num_core, choose_executor_memory, choose_driver_memory
from cads_sdk.iceberg.catalog import load_catalog
from cads_sdk.conf import get_hive_ip

try:
    catalog = load_catalog(
        "hive",
        **{
            "uri": get_hive_ip(),
        }
    )
except:
    print("Cannot load ccatalog")


def spark_dataframe_to_dwh(self, database, table_name, hdfs_path = "", file_format='iceberg',
                           repartition=False, numPartitions=None,
                           partition_by='', partition_date='',
                           compression='snappy', encrypt_columns=[], keys_path=''
                           ):
    """
    Store spark DataFrame object to datalake using spark


    Parameters
    ----------
    self
    database: metastore database name
    table_name: metastore table name
    hdfs_path: str

        .. deprecated:: 1.1.0
            Not support in the future, datalake 2.0 is not allowed

    file_format: str
        Default: iceberg

        File format when output value must be parquet|delta|iceberg

        .. deprecated:: 1.1.0
            Not support in the future, auto iceberg in datalake 2.0

    repartition: bool
        Write to folder with one file only

        Default False

        IF True:
            Write to folder with one file only

        If False:
            Number of file according to number executor cores
    partition_by: str
        Partition table by a column

    partition_date: str
        If Partition by a columns that not in dataframe
        That will auto partition by current_date

    compression: str
        Parquet compression

        Acceptable values include: none, uncompressed, snappy, gzip, lzo, brotli, lz4, zstd

    encrypt_columns: list
        List of columns need to encrypt

        Examples:
        >>> encrypt_columns = ['colA','colB']

    keys_path:
        Path to stored key

        .. deprecated:: 1.1.0
            Not support in the future, using parquet encryption instead


    Returns
    -------
    None or str


    Examples
    ----------
    .. code-block:: python

        import cads_sdk as cs

        df1 = cs.read_table("database.table_name")
        df1.to_dwh(
            hdfs_path="path/to/data/test1.delta", # just end path with delta then table will be store in delta format
            partition_by="m", # column time want to partition
            partition_date=ELT_DATE, # partition date
            database="database_name", # database name
            table_name="test1",
            repartition=True # table name
        )

    Function will store pandas object to Data warehouse with name database.test1
    """

    PS = get_spark()
    PS.store_spark_dataframe_to_dwh(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name,
                                    repartition=repartition, numPartitions=numPartitions,
                                    partition_by=partition_by, partition_date=partition_date,
                                    compression=compression, file_format=file_format,
                                    encrypt_columns=encrypt_columns, keys_path=keys_path)


def to_dwh(self, database, table_name, hdfs_path="",
           repartition=False, numPartitions=None,
           compression='snappy', file_format='iceberg', mode='overwrite',
           partition_by='', partition_date='', encrypt_columns=[], keys_path='', num_executors='1', parallel=True,
           engine='spark',
           existing_data_behavior='overwrite_or_ignore'):
    """
    Convert pandas dataframe into a table in datawarehouse


    Parameters
    ----------
    self
    database: metastore database name
    table_name: metastore table name
    hdfs_path: str

        .. deprecated:: 1.1.0
            Not support in the future, datalake 2.0 is not allowed

    file_format: str
        Default: iceberg

        File format when output value must be parquet|delta|iceberg

        .. deprecated:: 1.1.0
            Not support in the future, auto iceberg in datalake 2.0

    repartition: bool
        Write to folder with one file only

        Default False

        IF True:
            Write to folder with one file only

        If False:
            Number of file according to number executor cores
    partition_by: str
        Partition table by a column

    partition_date: str
        If Partition by a columns that not in dataframe
        That will auto partition by current_date

    compression: str
        Parquet compression

        Acceptable values include: none, uncompressed, snappy, gzip, lzo, brotli, lz4, zstd

    encrypt_columns: list
        List of columns need to encrypt

        Examples:
        >>> encrypt_columns = ['colA','colB']

    keys_path:
        Path to stored key

        .. deprecated:: 1.1.0
            Not support in the future, using parquet encryption instead

    engine: str
        Default: spark

        Value must be spark or arrow

    num_executors: spark resource

    file_format: spark resource

    parallel: spark resource

    Returns
    -------
    None or str


    Examples
    ----------
    .. code-block:: python

        # step 1 read data
        ELT_DATE = '2021-12-01'
        ELT_STR = ELT_DATE[:7]
        import pandas as pd
        df1 = pd.read_csv('./data.csv', sep='\t')


        import cads_sdk as cs

        # function to store to dwh
        df1.to_dwh(
            hdfs_path="path/to/data/test1.parquet/", # path hdfs
            partition_by="m", # column time want to partition
            partition_date=ELT_DATE, # partition date
            database="database_name", # database name
            table_name="test1", # table name
            repartition=True
        )

    Function store df1 to database_name.test1 at location "path/to/data/test1.delta"
    """
    if repartition:
        engine = 'spark'

    df_memory = self.memory_usage(index=True).sum() / 1024 / 1024

    if engine == 'spark' or 'delta' in hdfs_path.lower():
        if parallel:
            num_executors = choose_num_core(df_memory)

        driver_memory = choose_driver_memory(df_memory)
        executor_memory = choose_executor_memory(df_memory, int(num_executors))
        PS = get_spark(driver_memory=driver_memory, executor_memory=executor_memory, num_executors=num_executors)
        PS.to_dwh_spark(data=self, hdfs_path=hdfs_path, repartition=repartition,
                        numPartitions=numPartitions,
                        partition_by=partition_by, partition_date=partition_date,
                        compression=compression, file_format=file_format,
                        database=database, table_name=table_name,
                        encrypt_columns=encrypt_columns, keys_path=keys_path)
    elif engine == 'arrow':
        PyArrowWritter().to_dwh_pyarrow(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name,
                                 mode=mode,
                                 partition_by=partition_by, partition_date=partition_date,
                                 use_deprecated_int96_timestamps=True, existing_data_behavior=existing_data_behavior,
                                 encrypt_columns=encrypt_columns, keys_path=keys_path, catalog=catalog)
        # refresh_table_metadata(database=database, table_name=table_name, hdfs_path=hdfs_path, partition_by=partition_by)
    else:
        raise ValueError(f"engine must be spark or arrow but got: {engine}")


def write_json(data, path):
    """
    Function to write json object to datalake


    Parameters
    ----------
    data: Json object
    path: str
        Hdfs path


    Returns
    -------
    None or str


    Examples
    -----------

    .. code-block:: python

        import cads_sdk as cs
        json__file = cs.read_json('/path/to/file.json')
        ss.write_json(data, '/path/to_file.json')
    """
    # ========================LINEAGE======================
    try:
        from cads_sdk.pyspark.pylineage import emitPythonJob
        emitPythonJob(hdfs_path=path, outputNode=True)
    except:
        pass
    # =====================================================
    return PyArrowWritter().write_json(data=data, path=path)


def to_dwh_pyarrow(self, database, table_name, hdfs_path="", partition_by='', partition_date='',
                   use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore',
                   encrypt_columns=[], keys_path=''):
    """
    Store pandas object to datalake using pyarrow


    Parameters
    ----------
    self
    hdfs_path
    database
    table_name
    partition_by
    partition_date
    use_deprecated_int96_timestamps
    existing_data_behavior
    encrypt_columns
    keys_path


    Returns
    -------


    Examples:
    ----------

    """
    PyArrowWritter().to_dwh_pyarrow(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name,
                             partition_by=partition_by,
                             partition_date=partition_date,
                             use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
                             existing_data_behavior=existing_data_behavior, encrypt_columns=encrypt_columns,
                             keys_path=keys_path)
    # refresh_table_metadata(database=database, table_name=table_name, hdfs_path=hdfs_path, partition_by=partition_by)
