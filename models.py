from sqlalchemy import Column,Integer, String, JSON, Interval, DateTime

from database import Base


class Calculation(Base):
    __tablename__ = "calculation"

    id = Column(Integer, primary_key=True, index=True, )
    result = Column(JSON, default=None)
    status = Column(String, default="В очереди")
    start_date = Column(DateTime)
    lead_time = Column(Interval)
    calculation_name = Column(String)