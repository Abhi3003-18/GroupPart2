from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    rating = Column(Integer, nullable=False)
    review = Column(String(500), nullable=True)

    sandwich = relationship("Sandwich", back_populates="reviews")
