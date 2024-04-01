import json
import pyarrow as pa
from pyarrow import fs
from pyarrow import parquet as pq
import pandas as pd
# from cads_sdk.pyspark.pyspark_add_on import PySpark
from cads_sdk.utils import choose_num_core, choose_executor_memory, choose_driver_memory, \
    _check_series_convert_timestamps_internal, _get_local_timezone, contains_duplicates, modulereload, get_today, \
    query_yes_no
from cads_sdk.pyarrow.pandas_type import _ConvertPandasToParquet


class Utf8Encoder(object):
    def __init__(self, fp):
        self.fp = fp

    def write(self, data):
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        self.fp.write(data)


class PyArrow:
    def __init__(self, existing_data_behavior='overwrite_or_ignore'):
        # Install latest Pyarrow version
        import os
        from ..conf import (HADOOP_HOST, HADOOP_PORT)
        if HADOOP_HOST and HADOOP_PORT:
            self.hdfs = fs.HadoopFileSystem(host=HADOOP_HOST, port=int(HADOOP_PORT))
            self.existing_data_behavior = existing_data_behavior
        else:
            self.hdfs = fs.LocalFileSystem()

    def _check_is_file(self, hdfs_path):
        check = self.hdfs.get_file_info(hdfs_path)
        if check.type._name_ in ["Directory", "File"]:
            return True
        else:
            return False


class PyArrowReader(PyArrow):
    def __init__(self, existing_data_behavior='overwrite_or_ignore'):
        super().__init__(existing_data_behavior=existing_data_behavior)

    def read_key_from_json(self, keys_path, table_name, column_names: list = None):
        if self._check_is_file(keys_path):
            # Opening JSON file
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        keys_exist = {}
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            # check if key in file
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]
        return keys_exist

    def read_table(self, source, filters=''):
        if filters:
            return pq.read_table(source=source, filters=filters, filesystem=self.hdfs)
        else:
            return pq.read_table(source=source, filesystem=self.hdfs)

    def read_first_file(self, hdfs_path):
        '''
        Read schema pyarrow
        '''
        first_hdfs = pa.HadoopFileSystem().ls(hdfs_path)[-1]
        return self.read_table(source=first_hdfs)

    def read_json(self, path):
        with self.hdfs.open_input_file(path) as file:
            return json.load(file)


class PyArrowWritter(PyArrow):
    def __init__(self, existing_data_behavior='overwrite_or_ignore'):
        super().__init__(existing_data_behavior=existing_data_behavior)

    def write_json(self, data, path):
        with self.hdfs.open_output_stream(path) as file:
            json.dump(data, Utf8Encoder(file))

    @staticmethod
    def check_keys_path_format(keys_path):
        import re
        if re.search('json$', keys_path):
            return True
        else:
            raise Exception("keys_path must end with '.json'")

    @staticmethod
    def autogenerate_key(length_key=22):
        import string
        import random

        key = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length_key))
        key = key + "=="
        return key

    def write_append_keys_to_file(self, table_name, column_name='', keys_path='keys.json'):
        from datetime import datetime
        import json

        if self._check_is_file(keys_path):
            list_keys = PyArrowReader().read_json(keys_path)
        else:
            list_keys = []

        c = column_name
        keys = {}

        keys["name"] = f"secret_for_{table_name}_{c}"
        keys["description"] = ""
        keys["created"] = round(datetime.timestamp(datetime.now()))
        keys["material"] = self.autogenerate_key()
        list_keys.append(keys)

        with self.hdfs.open_output_stream(keys_path) as file:
            json.dump(list_keys, Utf8Encoder(file))

    def auto_generate_list_keys(self, table_name, column_name='', keys_path='keys.json'):
        from datetime import datetime

        if self._check_is_file(keys_path):
            list_keys = PyArrowReader().read_json(keys_path)
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

    def encrypt_column(self, data, table_name, column_names: list = None, keys_path=''):
        # check file keys exist
        keys_exist = PyArrowReader().read_key_from_json(keys_path=keys_path, table_name=table_name,
                                                        column_names=column_names)

        for c in column_names:
            # if not found key generate new key append to keys.json
            if c not in keys_exist.keys():
                print('Append key for', c)
                self.write_append_keys_to_file(table_name, c, keys_path)

        new_list_keys = PyArrowReader().read_key_from_json(keys_path=keys_path, table_name=table_name,
                                                           column_names=column_names)

        from cads_sdk.pandas.pandas_decrypt import encrypt_column
        for c in column_names:
            data[c] = data[c].encrypt_column(new_list_keys[c])

        return data

    @staticmethod
    def _check_series_convert_column_pyarrow(data, partition_by):

        new_type = {}

        # check column duplicated
        if contains_duplicates(data.columns):
            print("Columns is duplicated, check your data")

        for c in data.columns:
            if str(data[c].dtype) == 'category':
                if max(data[c].str.len()) == min(data[c].str.len()):
                    data[c] = pd.to_datetime(data[c])
            if c == partition_by:
                if c in data.columns:
                    if data[partition_by].dtype == 'object':
                        if len(data[c][0]) == 10:
                            new_type[partition_by] = pa.date64()
                    else:
                        new_type[c] = _ConvertPandasToParquet().get_type(str(data[c].dtype))
            else:
                data[c] = _check_series_convert_timestamps_internal(data[c], timezone=None)
                new_type[c] = _ConvertPandasToParquet().get_type(str(data[c].dtype))

        fields = [pa.field(x, y) for x, y in new_type.items()]
        new_schema = pa.schema(fields)
        table = pa.Table.from_pandas(
            data,
            schema=new_schema,
            preserve_index=False
        )

        return table

    @staticmethod
    def compare_data_type(first_sparkDF, second_sparkDF, partition_by):
        """
        Function to check when write data second time
        """
        error = {}
        first_sparkDF_schema = {}
        second_sparkDF_schema = {}

        for c in first_sparkDF.schema:
            c_name = c.name
            if partition_by == c_name and partition_by != '':
                continue
            first_sparkDF_schema[c.name] = c.type

        for c in second_sparkDF.schema:
            c_name = c.name
            if partition_by == c_name and partition_by != '':
                continue
            second_sparkDF_schema[c.name] = c.type

        if len(first_sparkDF_schema.keys()) != len(second_sparkDF_schema.keys()):
            print(f'First time have columns', first_sparkDF.schema.names)
            print(f'Second time have columns', second_sparkDF.schema.names)

            raise ValueError(
                f"First time have {len(first_sparkDF)} columns but second time have {len(second_sparkDF.schema)} columns")

        for c in second_sparkDF_schema.keys():
            second_type = second_sparkDF_schema[c]
            first_type = first_sparkDF_schema[c]

            if first_type != second_type:
                error[c] = {'first_time': first_type, 'second_time': second_type}

            if error.keys():
                print('Error', error)
                del first_sparkDF
                del second_sparkDF
                raise TypeError(f"DataType of Columns this time store is not like first time")
        print('Check schema OK')
        del first_sparkDF

    @staticmethod
    def write_df_to_table(adf, table, mode='overwrite'):
        if mode == 'overwrite':
            table.overwrite(adf)
        elif mode == 'append':
            table.append(adf)
        else:
            raise Exception(f"Write mode should be overwrite or append but got {mode}")

    @staticmethod
    def remove_field_from_schema(schema, field_name):
        from pyiceberg.schema import Schema
        new_fields = []
        for i in range(len(schema.fields)):
            if schema.fields[i].name != field_name:
                new_fields.append(schema.fields[i])

        return Schema(*new_fields)

    def create_table_if_not_exists(self, database, table_name, adf, catalog, partition_by):

        all_tables = catalog.list_tables(database)
        if (database, table_name) in all_tables:
            return catalog.load_table(database + "." + table_name)
        else:
            if partition_by:

                iceberg_schema = self.create_iceberg_schema(adf=adf)
                print("DEBUG iceberg_schema", iceberg_schema)
                partition_spec = self.create_partition_spec(schema=iceberg_schema, partition_by=partition_by)
                iceberg_schema = self.remove_field_from_schema(schema=iceberg_schema, field_name=partition_by)
                print("DEBUG iceberg_schema", iceberg_schema)
                return catalog.create_table(database + "." + table_name, schema=iceberg_schema,
                                            partition_spec=partition_spec)
            else:
                return catalog.create_table(database + "." + table_name, schema=adf.schema)

    @staticmethod
    def create_iceberg_schema(adf):
        return visit_pyarrow(adf.schema, _ConvertToIcebergWithoutIDs())

    @staticmethod
    def find_source_id(partition_by, schema):
        for f in schema.fields:
            if f.name == partition_by:
                source_id = f.field_id
                return source_id
        raise Exception(f"Cannot find field {partition_by} in schema: {schema}")

    def create_partition_spec(self, schema, partition_by):
        from pyiceberg.partitioning import PartitionSpec, PartitionField
        from pyiceberg.transforms import IdentityTransform
        return PartitionSpec(
            PartitionField(
                source_id=self.find_source_id(partition_by=partition_by, schema=schema),
                # This should match the source ID of the DataFrame's schema
                field_id=-1,  # This should match the field ID of the DataFrame's schema for "colA"
                transform=IdentityTransform(),
                name=partition_by
            )
        )

    def to_dwh_pyarrow(self, data, hdfs_path, database, table_name, mode='overwrite', partition_by='',
                       partition_date='',
                       use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore',
                       encrypt_columns: list = None, keys_path='', catalog=None):

        # old method still work this way
        # new method use pyarrow parquet encryption

        # old method
        if encrypt_columns:
            if keys_path:
                if self.check_keys_path_format(keys_path):
                    data = self.encrypt_column(data=data, table_name=table_name, column_names=encrypt_columns,
                                               keys_path=keys_path)
            else:
                raise Exception("You must add parameters keys_path=")

        if partition_by:
            raise Exception("Not support partition table for engine arrow yet, use engine spark instead")

            if partition_by in data.columns:
                adf = self._check_series_convert_column_pyarrow(data, partition_by)
            else:
                if not partition_date:
                    query_yes_no("""You should config partition_date, default today \nContinues Y/n?""")
                    partition_date = get_today()

                data[partition_by] = pd.to_datetime(partition_date)
                adf = self._check_series_convert_column_pyarrow(data, partition_by)

            print('HDFS path: ', hdfs_path)

            if self.check_is_file(hdfs_path):
                self.compare_data_type(self.read_first_file(hdfs_path), adf, partition_by)

            tbl = self.create_table_if_not_exists(database, table_name, adf, catalog, partition_by)
            self.write_df_to_table(adf=adf, table=tbl, mode=mode)

            # pq.write_to_dataset(
            #     adf,
            #     root_path=hdfs_path,
            #     partition_cols=[partition_by],
            #     use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
            #     filesystem=self.hdfs,
            #     existing_data_behavior=existing_data_behavior
            # )

        else:
            adf = self._check_series_convert_column_pyarrow(data, partition_by='')
            tbl = self.create_table_if_not_exists(database, table_name, adf, catalog, partition_by)
            self.write_df_to_table(adf=adf, table=tbl, mode=mode)

            # pq.write_to_dataset(
            #     adf,
            #     root_path=hdfs_path,
            #     use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
            #     filesystem=self.hdfs,
            #     existing_data_behavior=existing_data_behavior
            # )


from cads_sdk.iceberg.pyarrow import visit_pyarrow, _ConvertToIceberg


class _ConvertToIcebergWithoutIDs(_ConvertToIceberg):
    """
    Converts PyArrowSchema to Iceberg Schema with all -1 ids.

    The schema generated through this visitor should always be
    used in conjunction with `new_table_metadata` function to
    assign new field ids in order. This is currently used only
    when creating an Iceberg Schema from a PyArrow schema when
    creating a new Iceberg table.
    """

    @staticmethod
    def convertToNumber(s: str):
        return int.from_bytes(s.encode(), 'little')

    def _field_id(self, field: pa.Field) -> int:
        return _ConvertToIcebergWithoutIDs.convertToNumber(field.name)
