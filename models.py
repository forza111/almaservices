from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from database import Base


class Calculation(Base):
    __tablename__ = "calculation"

    id = Column(Integer, primary_key=True, index=True, )
    result = Column(JSON)