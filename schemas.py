import datetime
from datetime import timedelta

from pydantic import BaseModel, Json, validator, ValidationError,root_validator
from fastapi import HTTPException

class CalcCreate(BaseModel):
    id: int

class CalcResult(BaseModel):
    date_strt: datetime.date
    date_fin: datetime.date
    lag: int

    @root_validator
    def check_correct_data(cls, v):
        date_strt = v.get('date_strt')
        date_fin = v.get('date_fin')
        lag = v.get('lag')
        if lag <= 0:
            raise HTTPException(status_code=400, detail=f"field lag must be greater than zero, you passed {lag}")
        if date_strt >= date_fin:
            raise HTTPException(status_code=400, detail="Field date_fin must be larger than field date_strt")
        return v

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