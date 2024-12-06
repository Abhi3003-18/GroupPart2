from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models.resources import Resource as ResourceModel
from ..schemas.resources import ResourceCreate, ResourceUpdate


def create(db: Session, request: ResourceCreate):
    # Check for duplicate resource items
    existing_resource = db.query(ResourceModel).filter(ResourceModel.item == request.item).first()
    if existing_resource:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource with this item already exists")

    # Create a new resource
    new_resource = ResourceModel(
        item=request.item,
        amount=request.amount,
    )
    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_resource


def read_all(db: Session):
    try:
        resources = db.query(ResourceModel).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resources


def read_one(db: Session, resource_id: int):
    try:
        resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resource


def update(db: Session, resource_id: int, request: ResourceUpdate):
    try:
        resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id)
        if not resource.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

        # Check for duplicate resource item if updating item name
        if request.item:
            existing_resource = db.query(ResourceModel).filter(ResourceModel.item == request.item).first()
            if existing_resource and existing_resource.id != resource_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource with this item already exists")

        # Perform the update
        update_data = request.dict(exclude_unset=True)
        resource.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return resource.first()


def delete(db: Session, resource_id: int):
    try:
        resource = db.query(ResourceModel).filter(ResourceModel.id == resource_id)
        if not resource.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        resource.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def check_ingredient_availability(db: Session):
    try:
        low_resources = db.query(ResourceModel).filter(ResourceModel.amount <= 5).all()  # Threshold: 5 units
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return low_resources
