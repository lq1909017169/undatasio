from typing import List, Dict
from pydantic import BaseModel, ConfigDict
import pandas as pd


class Response(BaseModel):
    code: int
    msg: str | None
    data: List | None | Dict | str | pd.DataFrame

    model_config = ConfigDict(arbitrary_types_allowed=True)
