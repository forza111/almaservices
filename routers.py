from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from crud import calculation
from database import get_db
from models import Calculation
import schemas


router = APIRouter(tags=["Calculations API"])

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

@router.get('/calculation/{id}',response_model=schemas.CalcDetail, response_model_exclude_none=True)
async def get_detail_calculation(id: int, name: Optional[bool]=None, lead_time: Optional[bool]=None, db: Session = Depends(get_db)):
    calculations = db.query(Calculation).get(id)
    response = {
        "start_date": calculations.start_date,
        "status": calculations.status,
        "result": calculations.result,
    }
    if not name and not lead_time:
        return response
    if name and lead_time:
        response["calculation_name"] = calculations.calculation_name
        response["lead_time"] = calculations.lead_time
        return response
    if name:
        response["calculation_name"] = calculations.calculation_name
        return response
    if lead_time:
        response["lead_time"] = calculations.lead_time
        return response
