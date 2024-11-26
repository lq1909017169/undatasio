from typing import List, Dict
import pandas as pd


class Response:

    def __init__(self, code: int | None = None, msg: str | None = None,
                 data: List | None | Dict | str | pd.DataFrame = None):
        self.code = code
        self.msg = msg
        self.data = data
