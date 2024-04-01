from pyiceberg.table import Optional
from pyiceberg.table import Tuple

from cads_sdk.pyarrow.pyarrow_add_on import PyArrowReader
from cads_sdk.iceberg.catalog import load_catalog
from .add_on import get_location_from_table, render_filters_pyarrow, get_spark
from .conf import get_hive_ip
from .utils import log

try:
    catalog = load_catalog(
        "hive",
        **{
            "uri": get_hive_ip(),
        }
    )
except:
    print("Cannot load ccatalog")


######################
def read_table(full_table_name: str, selected_fields: Tuple[str, ...] = ("*",), limit: Optional[int] = None):
    """
    Convert a table in DWH to cads_sdk.Table


    Parameters
    ----------

    full_table_name: str
        Full table name in format database.table_name
    selected_fields: selected_fields: Tuple[str, ...]
        Default: None

        fields, column need to select
    limit: limit: Optional[int]
        Default: None

        Limit row need to select
        Examples: 100

    Returns
    -------
    cads_sdk.Table


    Examples
    --------
    .. code-block: python
    >>> import cads_sdk as cs
    >>> table = cs.read_table("database.table_name")
    >>> df = table.to_arrow()
    >>> df = table.to_spark()

    >>> import cads_sdk as cs
    >>> table = cs.read_table("database.table_name", limit=100, selected_fields=('colA'))
    >>> df = table.to_arrow()
    >>> df = table.to_spark()
    """
    return catalog.load_table(full_table_name).scan(selected_fields=selected_fields, limit=limit)


def sql(query: str):
    """
    Convert a SQL in spark.DataFrame object


    Parameters
    ----------
    query: str
        SQL query state



    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.sql("SELECT * FROM database.table_name WHERE d = current_date LIMIT 100")
    """
    PS = get_spark()
    return PS.spark.sql(query)


def read_table_pd(full_table_name, engine='spark', filters: str = None,
                  selected_fields: Tuple[str, ...] = ("*",), limit: Optional[int] = None):
    """
    Convert a table to pandas object


    Parameters
    ----------

    full_table_name: str
        Full table name in format database.table_name

    engine: str
        Default: spark
    filters: str
        Default: None

        Logic in sql format need to filter

        Examples: filters = "d = current_date"

    selected_fields: selected_fields: Tuple[str, ...]
        Default: None

        fields, column need to select
    limit: limit: Optional[int]
        Default: None

        Limit row need to select

        Examples: 100



    Returns
    -------
    pandas.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> import pandas as pd
    >>> pdf = pd.read_table("database.table_name", filter="d='2023-01-01'")
    >>> pdf = cs.read_table_pd("database.table_name", filter="d='2023-01-01'")
    """
    # ========================LINEAGE======================
    try:
        from cads_sdk.pyspark.pylineage import emitPythonJob
        emitPythonJob(full_table_name=full_table_name, outputNode=False)
    except:
        pass
    # =====================================================
    if engine == 'arrow':
        return read_table(full_table_name=full_table_name, selected_fields=selected_fields, limit=limit).to_pandas()

    elif engine == 'spark':
        PS = get_spark()
        if filters:
            filters = 'where ' + filters

        df_spark = PS.spark.sql(f"select * from {full_table_name} {filters}")
        df = df_spark.toPandas()
        return df
    raise ValueError(f"engine must by arrow, spark but got {engine}")


def read_dwh(full_table_name: str, filters: str = None):
    """
    Read table from dwh as spark.sql.DataFrame


    Parameters
    ----------
    full_table_name: str
        Full table name in format database.table_name
    filters: str
        Default: None

        Filter statement to limit data


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> import pandas as pd
    >>> df = cs.read_dwh("database.table_name", filter="d='2023-01-01'")
    """

    PS = get_spark()
    if filters:
        filters = 'where ' + filters
    df_spark = PS.spark.sql(f"select * from {full_table_name} {filters}")
    return df_spark


def read_csv(path, sep: str = ',', header=True):
    """
    Convert csv file in Datalake to spark.sql.DataFrame


    Parameters
    ----------
    path: str
        Absolute path of csv file
    sep: str
        Default: ','
        Seperator
    header: bool
        Default: True

        If True:
        Get first line as headers


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.read_csv("file:/home/user/a.csv", sep='\t')
    """
    PS = get_spark()
    return PS.read_csv(path=path, sep=sep, header=header)


def read_parquet(path):
    """
    Read parquet file from datalake as spark.sql.DataFrame

    Parameters
    ----------
    path: str
        Absolute path of parquet file


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.read_parquet("file:/home/user/a.parquet")
    >>> df = cs.read_parquet("hdfs:/home/user/a.parquet")
    """
    log("read parqet", "you should use read_table function instead if it is table read_parquet will get wrong result")
    PS = get_spark()
    return PS.read_parquet(path=path)


def read_json(path):
    """
    Convert a JSON file from datalake as spark.sql.DataFrame


    Parameters
    ----------
    path: str
        Absolute path of json file


    Returns
    -------
    Json


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.read_json("file:/home/user/a.json", sep='\t')
    """
    return PyArrowReader().read_json(path)


def refresh_table(full_table_name: str):
    """
    Refresh table if table is parquet and update metadata

    .. deprecated:: 1.1.0
        Not support in the future, with iceberg no need to refresh table

    Parameters
    ----------
    full_table_name: str


    """
    PS = get_spark()
    return PS.spark.sql(f"""REFRESH TABLE {full_table_name}""")