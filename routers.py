from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

import crud
from database import get_db
from models import Calculation
import schemas


router = APIRouter(tags=["Calculations API"])

@router.post('/create_calculations')
async def create_calculations_data(
        data: schemas.CalcResult,
        background_tasks: BackgroundTasks,
        id: schemas.CalcCreate = Depends(crud.create_id_calc),
        db: Session = Depends(get_db)
):
    background_tasks.add_task(crud.create_calc, db, data, id)
    return {"id": id}

@router.get('/calculations', response_model=List[schemas.CalcList])
async def get_last_calculations(db: Session = Depends(get_db)):
    db_calculations = crud.get_last_calc(db)
    return db_calculations

@router.get('/calculation/{id}', response_model=schemas.CalcDetail, response_model_exclude_none=True)
async def get_detail_calculation(
        id: int,
        name: Optional[bool] = None,
        lead_time: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    response = db.query(Calculation).get(id)
    if not name:
        response.calculation_name = None
    if not lead_time:
        response.lead_time = None
    return response
