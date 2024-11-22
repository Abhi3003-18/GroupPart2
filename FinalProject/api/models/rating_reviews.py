from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from api.dependencies.database import Base


class RatingReview(Base):
    __tablename__ = 'ratings_reviews'
    review_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    review = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
