from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    tracking_number = Column(String, unique=True)
    status = Column(String, nullable=False)
    total_price = Column(Float, nullable=False)