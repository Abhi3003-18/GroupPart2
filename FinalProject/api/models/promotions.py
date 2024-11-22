from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base
class Promotion(Base):
    __tablename__ = 'promotions'
    promotion_code = Column(String, primary_key=True)
    expiration_date = Column(Date, nullable=False)