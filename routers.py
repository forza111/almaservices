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
    """
    ## Выполнение расчета kernel.py в фоновом режиме и запись результатов

    Query Parameters
    ----------
    data:
    * date_start: datetime.date
    * date_fin: datetime.date
    * lag: int

    Returns
    -------
    JSON:
    * id - идентификатор расчета, запущенного в работу
    """
    background_tasks.add_task(crud.create_calc, db, data, id)
    return {"id": id}

@router.get('/calculations', response_model=List[schemas.CalcList])
async def get_last_calculations(db: Session = Depends(get_db)):
    """
    ## Получение 10 последних запущенных расчетов

    Returns
    -------
    JSON:
    [
    * calculation_name - имя расчета
    * start_date - дата запуска расчета
    * status - статус расчета
    ]
    """
    db_calculations = crud.get_last_calc(db)
    return db_calculations

@router.get('/calculation/{id}', response_model=schemas.CalcDetail, response_model_exclude_none=True)
async def get_detail_calculation(
        id: int,
        name: Optional[bool] = None,
        lead_time: Optional[bool] = None,
        db: Session = Depends(get_db)
):
    """
    ## Получение подробной информации о расчете

    Path Parameters
    ----------
    * id: int - идентификатор искомого расчета

    Query Parameters
    ----------
    * name: bool(Optional) - необходимость в выводе имени расчета
    * lead_time: bool(Optional) - необходимость в выводе времени выполнения расчета

    Returns
    -------
    JSON:
    * start_date - дата запуска расчета
    * status - статус расчета
    * result - результат расчета
    * calculation_name - имя расчета (Опционально)
    * lead_time - время выполнения расчета (Опционально)
    """
    response = db.query(Calculation).get(id)
    if not name:
        response.calculation_name = None
    if not lead_time:
        response.lead_time = None
    return response
