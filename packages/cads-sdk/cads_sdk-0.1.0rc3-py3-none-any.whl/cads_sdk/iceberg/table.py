from typing import (
    TYPE_CHECKING
)
from pyiceberg.table import DataScan as DataScanIceberg
from pyiceberg.table import Union, BooleanExpression, ALWAYS_TRUE, Optional, Properties, EMPTY_DICT
from pyiceberg.table import Table as IcebergTable
from pyiceberg.table import TableMetadata, Tuple, Field, FileIO

import pyspark as ps
import pyarrow as pa

if TYPE_CHECKING:
    from cads_sdk.iceberg.catalog import Catalog

Identifier = Tuple[str, ...]


class DataScan(DataScanIceberg):
    def __init__(
        self,
        table: IcebergTable,
        row_filter: Union[str, BooleanExpression] = ALWAYS_TRUE,
        selected_fields: Tuple[str, ...] = ("*",),
        case_sensitive: bool = True,
        snapshot_id: Optional[int] = None,
        options: Properties = EMPTY_DICT,
        limit: Optional[int] = None,
    ):

        super().__init__(table=table, row_filter=row_filter, selected_fields=selected_fields,
                         case_sensitive=case_sensitive, snapshot_id=snapshot_id, options=options, limit=limit)

    def to_spark(self) -> ps.sql.dataframe.DataFrame:
        from cads_sdk.pyspark.pyspark_add_on import PySpark
        PS = PySpark()
        return PS.project_table(table=self.table, row_filter=self.row_filter, limit=self.limit)

    def to_arrow(self) -> pa.Table:
        from cads_sdk.iceberg.pyarrow import project_table

        return project_table(
            self.plan_files(),
            self.table,
            self.row_filter,
            self.projection(),
            case_sensitive=self.case_sensitive,
            limit=self.limit,
        )

    def __repr__(self) -> str:
        """Return the string representation of the Table class."""
        return self.table.__repr__()


class Table(IcebergTable):
    def __init__(
        self, identifier: Identifier, metadata: TableMetadata, metadata_location: str, io: FileIO, catalog
    ) -> None:
        super().__init__(identifier=identifier, metadata=metadata, metadata_location=metadata_location,
                         io=io, catalog=catalog)

    def scan(
        self,
        row_filter: Union[str, BooleanExpression] = ALWAYS_TRUE,
        selected_fields: Tuple[str, ...] = ("*",),
        case_sensitive: bool = True,
        snapshot_id: Optional[int] = None,
        options: Properties = EMPTY_DICT,
        limit: Optional[int] = None,
    ) -> DataScan:
        return DataScan(
            table=self,
            row_filter=row_filter,
            selected_fields=selected_fields,
            case_sensitive=case_sensitive,
            snapshot_id=snapshot_id,
            options=options,
            limit=limit,
        )





