import datetime
from pydantic import BaseModel

class CalcCreate(BaseModel):
    id: int


class CalcResult(BaseModel):
    date_strt: datetime.date
    date_fin: datetime.date
    lag: int

class CalcStatus(BaseModel):
    status: str