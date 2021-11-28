from sqlalchemy.orm import Session

import models, schemas
from kernel import calc


def create_calc(db: Session, data: schemas.Data):
    res = calc(data.date_strt, data.date_fin, data.lag)
    db_calc = models.Calculation(result=res)
    db.add(db_calc)
    db.commit()
    db.refresh(db_calc)
    return db_calc

print()