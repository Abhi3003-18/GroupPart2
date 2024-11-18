from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas


def create_resource(db: Session, resource: schemas.ResourceCreate):
    new_resource = models.Resource(
        item=resource.item,
        amount=resource.amount
    )
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource


def update_resource(db: Session, resource_id: int, resource: schemas.ResourceUpdate):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    for var, value in vars(resource).items():
        setattr(db_resource, var, value) if value is not None else None
    db.commit()
    return db_resource


def delete_resource(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(db_resource)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def read_all_resources(db: Session):
    return db.query(models.Resource).all()


def read_one_resource(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource