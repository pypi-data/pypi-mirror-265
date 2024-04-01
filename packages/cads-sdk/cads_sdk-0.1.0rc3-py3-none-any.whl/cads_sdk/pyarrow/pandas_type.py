class _ConvertPandasToParquet:
    TYPE_MAPPER = {
        'object': 'STRING',
        'float64': 'DOUBLE',
        'float32': 'DOUBLE',
        'int64': 'INT64',
        'int32': 'INT32',
        'bool': 'BOOLEAN',
        'datetime64': 'timestamp[s]',
        'datetime64[ns]': 'timestamp[s]',
        'datetime64[ns, Asia/Jakarta]': 'timestamp[s]',
        'datetime64[ns, UTC]': 'timestamp[s]'
    }

    def get_type(self, pandas_type):
        if pandas_type in self.TYPE_MAPPER:
            return self.TYPE_MAPPER[pandas_type]
        else:
            raise TypeError(f"Not suppport {pandas_type} yet, df.dtype to check your type")