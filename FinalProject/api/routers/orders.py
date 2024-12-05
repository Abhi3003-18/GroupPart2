from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/revenue/", response_model=dict)
def get_revenue(start_date: str, end_date: str, db: Session = Depends(get_db)):
    return controller.calculate_revenue(db, start_date=start_date, end_date=end_date)

@router.get("/track/{order_id}", response_model=dict)
def track_order(order_id: int, db: Session = Depends(get_db)):
    return track_order(db=db, order_id=order_id)

@router.put("/{order_id}/apply-promo/", response_model=dict)
def apply_promo(order_id: int, promo_code: str, db: Session = Depends(get_db)):
    return apply_promo_code(db=db, order_id=order_id, promo_code=promo_code)
