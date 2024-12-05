from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers.resources import create, read_all, read_one, update, delete
from ..schemas.resources import ResourceCreate, ResourceUpdate, Resource
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Resources'],
    prefix="/resources"
)

@router.post("/", response_model=Resource, status_code=status.HTTP_201_CREATED)
def create_resource(request: ResourceCreate, db: Session = Depends(get_db)):
    return create(db=db, request=request)

@router.get("/", response_model=list[Resource])
def get_all_resources(db: Session = Depends(get_db)):
    return read_all(db=db)

@router.get("/{resource_id}", response_model=Resource)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    return read_one(db=db, resource_id=resource_id)

@router.put("/{resource_id}", response_model=Resource)
def update_resource(resource_id: int, request: ResourceUpdate, db: Session = Depends(get_db)):
    return update(db=db, resource_id=resource_id, request=request)

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    return delete(db=db, resource_id=resource_id)

@router.get("/low-stock/", response_model=list[Resource])
def get_low_stock_resources(db: Session = Depends(get_db)):
    return check_ingredient_availability(db)
