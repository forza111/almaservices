from fastapi import APIRouter, BackgroundTasks, Depends
from time import sleep
from sqlalchemy.orm import Session

import schemas
from kernel import calc
from database import get_db
from crud import calculation


router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post('/')
async def get_user_repos(data: schemas.Data, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # date_start  = data.date_strt
    # date_fin = data.date_fin
    # lag = data.lag
    # background_tasks.add_task(calc, date_start,date_fin,lag)
    background_tasks.add_task(calculation.create_calc, db, data)
    return {"id": 1}

