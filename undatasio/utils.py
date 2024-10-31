from typing import List, Dict
from pydantic import BaseModel, ConfigDict
import pandas as pd


class Response(BaseModel):
    code: int | None = None
    msg: str | None = None
    data: List | None | Dict | str | pd.DataFrame = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
