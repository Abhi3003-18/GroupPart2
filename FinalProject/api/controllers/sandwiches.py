from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models.sandwiches import Sandwich as SandwichModel
from ..schemas.sandwiches import SandwichCreate, SandwichUpdate


def create(db: Session, request: SandwichCreate):
    # Check if a sandwich with the same name already exists
    existing_sandwich = db.query(SandwichModel).filter(SandwichModel.sandwich_name == request.sandwich_name).first()
    if existing_sandwich:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sandwich with this name already exists")

    # Create the new sandwich
    new_sandwich = SandwichModel(
        sandwich_name=request.sandwich_name,
        price=request.price,
    )
    try:
        db.add(new_sandwich)
        db.commit()
        db.refresh(new_sandwich)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_sandwich


def read_all(db: Session):
    try:
        sandwiches = db.query(SandwichModel).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return sandwiches


def read_one(db: Session, sandwich_id: int):
    try:
        sandwich = db.query(SandwichModel).filter(SandwichModel.id == sandwich_id).first()
        if not sandwich:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return sandwich


def update(db: Session, sandwich_id: int, request: SandwichUpdate):
    try:
        sandwich = db.query(SandwichModel).filter(SandwichModel.id == sandwich_id)
        if not sandwich.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")

        # Check for duplicate sandwich name if updating name
        if request.sandwich_name:
            existing_sandwich = db.query(SandwichModel).filter(SandwichModel.sandwich_name == request.sandwich_name).first()
            if existing_sandwich and existing_sandwich.id != sandwich_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sandwich with this name already exists")

        # Perform the update
        update_data = request.dict(exclude_unset=True)
        sandwich.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return sandwich.first()


def delete(db: Session, sandwich_id: int):
    try:
        sandwich = db.query(SandwichModel).filter(SandwichModel.id == sandwich_id)
        if not sandwich.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
        sandwich.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def search_sandwiches(db: Session, query: str):
    try:
        sandwiches = db.query(SandwichModel).filter(SandwichModel.sandwich_name.ilike(f"%{query}%")).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return sandwiches
