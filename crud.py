import time

from fastapi import Depends
from sqlalchemy.orm import Session

import datetime
import models
import schemas
from kernel import kern
from database import get_db


def create_calc(db: Session, data: schemas.CalcResult, id: schemas.CalcCreate):
    """Передача полученных для расчета данных в kernel.py и запись полученных данных в БД."""
    start_time = time.time()
    db_calc = db.query(models.Calculation).get(id)
    db_calc.status = "Идет расчет"
    db_calc.start_date = datetime.datetime.now()
    db_calc.calculation_name = f"calculation_{id}"
    db.add(db_calc)
    db.commit()
    res = kern(data.date_strt, data.date_fin, data.lag)
    db_calc.result = res
    db_calc.status = "Завершен"
    db_calc.lead_time = str(time.time() - start_time)
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc

def create_id_calc(db: Session = Depends(get_db)):
    """
    Создание пустой записи в БД и возврат идентификатора
    """
    db_id_calc = models.Calculation()
    db.add(db_id_calc)
    db.commit()
    db.refresh(db_id_calc)
    return db_id_calc.id

def get_last_calc(db: Session):
    """
    Получение 10 последних запущенных расчетов
    """
    calculations = db.query(models.Calculation).order_by(models.Calculation.start_date.desc()).limit(10).all()
    return calculations