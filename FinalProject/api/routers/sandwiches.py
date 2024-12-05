from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from ..controllers.sandwiches import create, read_all, read_one, update, delete
from ..schemas.sandwiches import SandwichCreate, SandwichUpdate, Sandwich
from ..dependencies.database import get_db

router = APIRouter(
    tags=['Sandwiches'],
    prefix="/sandwiches"
)

@router.post("/", response_model=Sandwich, status_code=status.HTTP_201_CREATED)
def create_sandwich(request: SandwichCreate, db: Session = Depends(get_db)):
    return create(db=db, request=request)

@router.get("/", response_model=list[Sandwich])
def get_all_sandwiches(db: Session = Depends(get_db)):
    return read_all(db=db)

@router.get("/{sandwich_id}", response_model=Sandwich)
def get_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return read_one(db=db, sandwich_id=sandwich_id)

@router.put("/{sandwich_id}", response_model=Sandwich)
def update_sandwich(sandwich_id: int, request: SandwichUpdate, db: Session = Depends(get_db)):
    return update(db=db, sandwich_id=sandwich_id, request=request)

@router.delete("/{sandwich_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    return delete(db=db, sandwich_id=sandwich_id)

@router.get("/search/", response_model=list[Sandwich])
def search_sandwiches(query: str, db: Session = Depends(get_db)):
    return search_sandwiches(db=db, query=query)
