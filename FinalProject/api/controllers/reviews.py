from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from ..models.reviews import Review as ReviewModel
from ..schemas.reviews import ReviewCreate


def create_review(db: Session, request: ReviewCreate):
    new_review = ReviewModel(
        sandwich_id=request.sandwich_id,
        rating=request.rating,
        review=request.review,
    )
    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review


def read_reviews(db: Session):
    try:
        reviews = db.query(ReviewModel).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return reviews


def read_reviews_by_sandwich(db: Session, sandwich_id: int):
    try:
        reviews = db.query(ReviewModel).filter(ReviewModel.sandwich_id == sandwich_id).all()
        if not reviews:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found for this sandwich")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return reviews
