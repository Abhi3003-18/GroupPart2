from pydantic import BaseModel
from typing import Optional


class ReviewBase(BaseModel):
    sandwich_id: int
    rating: int
    review: Optional[str] = None


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True
