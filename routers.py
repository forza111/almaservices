from fastapi import APIRouter, BackgroundTasks
from time import sleep

import schemas
from kernel import calc

router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@router.post('/')
async def get_user_repos(data: schemas.Data, background_tasks: BackgroundTasks):
    date_start  = data.date_strt
    date_fin = data.date_fin
    lag = data.lag
    background_tasks.add_task(calc, date_start,date_fin,lag)
    return {"id": 1}

