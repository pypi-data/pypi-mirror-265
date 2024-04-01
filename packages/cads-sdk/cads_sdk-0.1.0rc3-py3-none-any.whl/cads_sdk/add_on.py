from typing import (Union)
from cads_sdk.pyspark.pyspark_add_on import PySpark

from cads_sdk.pyarrow import exists
from cads_sdk.pyspark.hive_metastore import HiveMetastoreClient
import os

from cads_sdk.utils import query_yes_no


def get_spark(driver_memory='2G', num_executors='4', executor_memory='4G', port='', yarn=False):
    """
    Quick start spark


    Parameters
    ----------
    driver_memory: str
        Default: '8G'

        spark driver memory
    num_executors: str
        Default: 4

        spark --num_executors
    executor_memory: str
        Default: 4G

        For mode yarn only
    port:
    yarn: bool

        If True:
        Run spark on master yarn

        If False:
        Run spark on master local



    Returns
    -------
    pyspark.SparkSession


    Examples
    -----------
    .. code-block:: python

        import cads_sdk as cs
        spark = cs.start()
    """
    return PySpark(driver_memory=driver_memory, num_executors=num_executors, executor_memory=executor_memory, yarn=yarn)


def refresh_table_metadata(database, table_name, hdfs_path, partition_by=''):
    PS = get_spark()
    PS.create_table_and_metadata(database=database, table_name=table_name, partition_by=partition_by, hdfs_path=hdfs_path)

    PS.spark.sql(f"""REFRESH TABLE {database}.{table_name}""")


def drop_table(full_table_name, engine='arrow'):
    if query_yes_no("Are you sure you want to drop table?", default='no'):
        provider = get_provider_from_table(full_table_name)
        if engine == 'spark':
            PS = get_spark()
            if provider not in ['delta', 'iceberg']:
                PS.spark.sql(f"""ALTER TABLE {full_table_name} SET TBLPROPERTIES('external.table.purge' = 'false')""")
            PS.spark.sql(f"DROP TABLE {full_table_name}")
        elif engine == 'arrow':
            from cads_sdk.reader import catalog
            catalog.drop_table(full_table_name)
        raise ValueError(f"engine must be arrow or spark but got {engine}")


def drop_table_and_delete_data(full_table_name: str, engine='spark'):
    """
    Delete data and
    Parameters
    ----------
    full_table_name
    engine

    Returns
    -------

    """
    if query_yes_no("Are you sure you want to drop table and delete data?", default='no'):
        provider = get_provider_from_table(full_table_name)
        if engine == 'spark':
            PS = get_spark()
            if provider not in ['delta', 'iceberg']:
                PS.spark.sql(f"""ALTER TABLE {full_table_name} SET TBLPROPERTIES('external.table.purge' = 'false')""")
            df = PS.spark.sql(f"DESCRIBE FORMATTED {full_table_name}").toPandas()
            location = df[df['col_name']=='Location']['data_type'].values[0]

            print(f"MOVE DATA {location} to /shared/trash")
            base_name = os.path.basename(location)
            if exists(f"/shared/trash/{base_name}"):
                os.system(f"hdfs dfs -rm -r /shared/trash/{base_name}")
            os.system(f"hdfs dfs -mv {location} /shared/trash")
            os.system(f"hdfs dfs -rm -r {location}")
            PS.spark.sql(f"DROP TABLE {full_table_name}")
        elif engine == 'arrow':
            from cads_sdk.reader import catalog
            location = get_location_from_table(full_table_name)

            print(f"MOVE DATA {location} to /shared/trash")
            base_name = os.path.basename(location)
            if exists(f"/shared/trash/{base_name}"):
                os.system(f"hdfs dfs -rm -r /shared/trash/{base_name}")
            os.system(f"hdfs dfs -mv {location} /shared/trash")
            os.system(f"hdfs dfs -rm -r {location}")
            catalog.drop_table(full_table_name)



######################
# dataframe function
#####################
def spark_dataframe_info(self):
    """

    Parameters
    ----------
    self


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    -----------

    >>> import cads_sdk as cs
    >>> df = cs.read_table("database.table_name")
    >>> df.info()
    +------+-----------+-------------+--------------+
    |column|total_count|is_null_count|percent_isnull|
    +------+-----------+-------------+--------------+
    |  colA|          2|            0|          0.0%|
    |  colB|          2|            0|          0.0%|
    |  colC|          2|            0|          0.0%|
    +------+-----------+-------------+--------------+
    """
    sdf = self
    sdf.createOrReplaceTempView('info_table')
    sql = ''

    column_names = sdf.schema.names

    if len(column_names) > 1:

        for c in column_names[:-1]:
            check_column = f"""
                SELECT '{c}' column,
                count(case when {c} is null or {c} is not null then 1 end) total_count, 
                count(case when {c} is null then 1 end) is_null_count,
                CONCAT(CAST(ROUND(count(case when {c} is null then 1 end) / count(case when {c} is not null or {c} is null then 1 end) * 100, 2) as STRING), '%') percent_isnull FROM info_table \n"""
            sql += check_column
            sql += 'UNION ALL \n'

    c=column_names[-1]
    check_column_end = f"""
                SELECT '{c}' column,
                count(case when {c} is null or {c} is not null then 1 end) total_count, 
                count(case when {c} is null then 1 end) is_null_count,
                CONCAT(CAST(ROUND(count(case when {c} is null then 1 end) / count(case when {c} is not null or {c} is null then 1 end)* 100, 2) as STRING), '%') percent_isnull FROM info_table \n"""
    sql += check_column_end
    PS = get_spark()
    return PS.spark.sql(sql)


def limit_timestamp(sparkDF):
    sql = ""
    for c in sparkDF.schema:
        if str(c.dataType) in ['TimestampType()', 'DateType()']:
            sql += f"AND {c.name} between '1900-01-01' AND '2300-01-01' \n"
    PS = PySpark()
    print("Filter")
    print(sql)
    sparkDF.createOrReplaceTempView('df')
    return PS.spark.sql(f"""SELECT * FROM df WHERE 1=1 {sql}""")


############ other table functions
def get_location_from_table(full_table_name: str):
    """
    Get location from table, path of table

    Parameters
    ----------
    full_table_name

    Returns
    -------

    """
    from cads_sdk.conf import get_hive_ip
    HIVE_IP_NODES1 = get_hive_ip()
    HIVE_IP_NODES1 = HIVE_IP_NODES1.replace("thrift://", "")
    HIVE = HiveMetastoreClient(hmss_ro_addrs=[HIVE_IP_NODES1])
    d, t = full_table_name.split('.')

    location = HIVE.get_table(db_name=d, tb_name=t).__dict__['sd'].__dict__['location']
    import re

    pattern = re.compile('/data/')
    x = pattern.search(location)

    location = location[x.start():]
    return location


def get_provider_from_table(full_table_name: str):
    """
    Get table type: parquet, iceberg, delta

    par
    """
    from cads_sdk.conf import get_hive_ip
    HIVE_IP_NODES1 = get_hive_ip()
    HIVE_IP_NODES1 = HIVE_IP_NODES1.replace("thrift://", "")
    HIVE = HiveMetastoreClient(hmss_ro_addrs=[HIVE_IP_NODES1])
    d, t = full_table_name.split('.')

    property = HIVE.get_table(db_name=d, tb_name=t).parameters
    if 'spark.sql.sources.provider' in property:
        return property['spark.sql.sources.provider'].lower()
    elif 'table_type' in property:
        return property['table_type'].lower()
    else:
        return None


def render_filters_pyarrow(sql):
    """
    function support read_dwh() by pyarrow engine, render sql where clause
    """
    if sql:
        import sqlglot
        sql = sqlglot.transpile(sql, write='spark', identify=True, pretty=True)[0]
        list_bool_expression = sql.split('\n')


        import re

        pattern_column = re.compile('`(.*?)`')
        pattern_operator = re.compile('[<>=]')


        list_filters = []
        for b in list_bool_expression:
            x1 = pattern_column.search(b)
            column_name = b[x1.start()+1: x1.end()-1]

            x2 = pattern_operator.search(b)
            operator = b[x2.start(): x2.end()]

            value = b[x2.end()+2: -1]

            list_filters.append((column_name, operator, value))

        return list_filters
    else:
        return ''


# function show pyspark
def show(self, n: int = 20, truncate: Union[bool, int] = 50, vertical: bool = False) -> None:
    """Prints the first ``n`` rows to the console.
    .. versionadded:: 1.3.0
    Parameters
    ----------
    n : int, optional
        Number of rows to show.
    truncate : bool or int, optional
        If set to ``True``, truncate strings longer than 20 chars by default.
        If set to a number greater than one, truncates long strings to length ``truncate``
        and align cells right.
    vertical : bool, optional
        If set to ``True``, print output rows vertically (one line
        per column value).
    Examples
    --------
    >>> df
    DataFrame[age: int, name: string]
    >>> df.show()
    +---+-----+
    |age| name|
    +---+-----+
    |  2|Alice|
    |  5|  Bob|
    +---+-----+
    >>> df.show(truncate=3)
    +---+----+
    |age|name|
    +---+----+
    |  2| Ali|
    |  5| Bob|
    +---+----+
    >>> df.show(vertical=True)
    -RECORD 0-----
     age  | 2
     name | Alice
    -RECORD 1-----
     age  | 5
     name | Bob
    """

    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("Parameter 'n' (number of rows) must be an int")

    if not isinstance(vertical, bool):
        raise TypeError("Parameter 'vertical' must be a bool")

    if isinstance(truncate, bool) and truncate:
        print(self._jdf.showString(n, 20, vertical))
    else:
        try:
            int_truncate = int(truncate)
        except ValueError:
            raise TypeError(
                "Parameter 'truncate={}' should be either bool or int.".format(truncate)
            )

        print(self._jdf.showString(n, int_truncate, vertical))


