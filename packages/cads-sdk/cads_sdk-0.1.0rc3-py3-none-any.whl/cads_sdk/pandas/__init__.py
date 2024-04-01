from ..writter import to_dwh
from .pandas_decrypt import decrypt, encrypt, decrypt_column, encrypt_column

import pandas as pd
from pandas import DataFrame
from pandas.core.series import Series
from ..utils import modulereload

DataFrame.to_dwh = to_dwh
# DataFrame._repr_html_ = PandasDataFrame_repr_html_

Series.decrypt_column = decrypt_column
modulereload(pd)

# TODO
#  write docs for pandas decrypt
