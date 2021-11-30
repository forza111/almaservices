from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from time import sleep
from sqlalchemy.orm import Session
from sqlalchemy import text

from models import Calculation
import schemas
from kernel import kern
from database import get_db
from crud import calculation


router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post('/')
async def create_calc_data(data: schemas.CalcResult, background_tasks: BackgroundTasks,
                         id: schemas.CalcCreate = Depends(calculation.create_id_calc),
                         db: Session = Depends(get_db)
                         ):
    background_tasks.add_task(calculation.create_calc, db, data, id)
    return {"id": id}

@router.get('/calculations',response_model=List[schemas.CalcList])
async def get_last_calculations(db: Session = Depends(get_db)):
    calculations = db.query(Calculation).order_by(Calculation.start_date.desc()).limit(10).all()
    return calculations

@router.get('/calculation/{id}')
async def get_detail_calculation(id: int, db: Session = Depends(get_db), name: bool = False, lead_time: bool = False):
    calculations = db.query.add_column(Calculation.calculation_name).get(id)
    # calculations = db.query(text(f"SELECT * FROM calculation WHERE calculation.id = {id}"))
    # calculations = db.execute(select(Calculation.start_date, Calculation.status, Calculation.result, Calculation.calculation_name))

    # if name:


    return calculations
