from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers.reviews import create_review, read_reviews, read_reviews_by_sandwich
from ..schemas.reviews import ReviewCreate, Review
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Reviews"],
    prefix="/reviews"
)

@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
def add_review(request: ReviewCreate, db: Session = Depends(get_db)):
    return create_review(db=db, request=request)

@router.get("/", response_model=list[Review])
def get_all_reviews(db: Session = Depends(get_db)):
    return read_reviews(db=db)

@router.get("/sandwich/{sandwich_id}", response_model=list[Review])
def get_reviews_by_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return read_reviews_by_sandwich(db=db, sandwich_id=sandwich_id)
