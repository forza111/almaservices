from fastapi import APIRouter, BackgroundTasks, Depends
from time import sleep
from sqlalchemy.orm import Session

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
