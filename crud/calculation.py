from fastapi import Depends
from sqlalchemy.orm import Session

import models, schemas
from kernel import kern
import database


def change_status_calc(id: schemas.CalcCreate, db: Session = Depends(database.get_db)):
    db_calc = db.query(models.Calculation).get(id)
    db_calc.status = "Идет расчет"
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc

def create_calc(db: Session, data: schemas.CalcResult, id: schemas.CalcCreate, status_update: schemas.CalcStatus = Depends(change_status_calc(id))):
    res = kern(data.date_strt, data.date_fin, data.lag)
    db_calc = db.query(models.Calculation).get(id)
    db_calc.result = res
    db_calc.status = "Завершен"
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc


def create_id_calc(db: Session = Depends(database.get_db)):
    db_id_calc = models.Calculation()
    db.add(db_id_calc)
    db.commit()
    db.refresh(db_id_calc)
    return db_id_calc.id

