import datetime
from pydantic import BaseModel


class Data(BaseModel):
    date_strt: datetime.date
    date_fin: datetime.date
    lag: int