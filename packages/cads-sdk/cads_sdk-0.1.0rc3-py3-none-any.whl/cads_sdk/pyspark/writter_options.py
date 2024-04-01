from pyspark.sql.utils import to_str
from pyspark.sql import DataFrameWriter


def sdk_options(self, options: "OptionalPrimitiveType") -> "DataFrameWriter":
    """
    Adds output options for the underlying data source.

    .. versionadded:: 1.4.0

    .. versionchanged:: 3.4.0
        Supports Spark Connect.

    Parameters
    ----------
    **options : dict
        The dictionary of string keys and primitive-type values.

    Examples
    --------
    >>> spark.range(1).write.option("key", "value")
    <...readwriter.DataFrameWriter object ...>

    Specify the option 'nullValue' and 'header' with writing a CSV file.

    >>> from pyspark.sql.types import StructType,StructField, StringType, IntegerType
    >>> schema = StructType([
    ...     StructField("age",IntegerType(),True),
    ...     StructField("name",StringType(),True),
    ... ])
    >>> import tempfile
    >>> with tempfile.TemporaryDirectory() as d:
    ...     # Write a DataFrame into a CSV file with 'nullValue' option set to 'Hyukjin Kwon',
    ...     # and 'header' option set to `True`.
    ...     df = spark.createDataFrame([(100, None)], schema=schema)
    ...     df.write.options(nullValue="Hyukjin Kwon", header=True).mode(
    ...         "overwrite").format("csv").save(d)
    ...
    ...     # Read the CSV file as a DataFrame.
    ...     spark.read.option("header", True).format('csv').load(d).show()
    +---+------------+
    |age|        name|
    +---+------------+
    |100|Hyukjin Kwon|
    +---+------------+
    """
    for k in options:
        self._jwrite = self._jwrite.option(k, to_str(options[k]))
    return self


DataFrameWriter.sdk_options = sdk_options