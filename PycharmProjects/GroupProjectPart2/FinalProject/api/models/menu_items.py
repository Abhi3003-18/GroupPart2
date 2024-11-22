from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = 'menu_items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    dish_name = Column(String, nullable=False)
    ingredients = Column(String)
    price = Column(Float, nullable=False)
    calories = Column(Integer)
    food_category = Column(String)
