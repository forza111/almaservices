import datetime
from datetime import timedelta

from pydantic import BaseModel, Json


class CalcCreate(BaseModel):
    id: int

class CalcResult(BaseModel):
    date_strt: datetime.date
    date_fin: datetime.date
    lag: int

class CalcStatus(BaseModel):
    status: str

class CalcList(BaseModel):
    calculation_name: str
    start_date: datetime.date
    status: str

    class Config:
        orm_mode = True

class CalcDetail(BaseModel):
    start_date: datetime.date
    status: str
    result: Json
    calculation_name: str = None
    lead_time: timedelta = None

    class Config:
        orm_mode = True
