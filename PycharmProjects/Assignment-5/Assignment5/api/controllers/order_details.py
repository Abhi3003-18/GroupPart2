from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status, Response
from ..models import models, schemas


def create_order_detail(db: Session, order_detail: schemas.OrderDetailCreate):
    new_order_detail = models.OrderDetail(
        amount=order_detail.amount,
        order_id=order_detail.order_id,
        sandwich_id=order_detail.sandwich_id
    )
    db.add(new_order_detail)
    db.commit()
    db.refresh(new_order_detail)
    return new_order_detail


def update_order_detail(db: Session, order_detail_id: int, order_detail: schemas.OrderDetailUpdate):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    for var, value in vars(order_detail).items():
        setattr(db_order_detail, var, value) if value is not None else None
    db.commit()
    return db_order_detail


def delete_order_detail(db: Session, order_detail_id: int):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    db.delete(db_order_detail)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def read_all_order_details(db: Session):
    return db.query(models.OrderDetail).options(joinedload(models.OrderDetail.sandwich)).all()


def read_one_order_detail(db: Session, order_detail_id: int):
    db_order_detail = db.query(models.OrderDetail).options(joinedload(models.OrderDetail.sandwich)).filter(models.OrderDetail.id == order_detail_id).first()
    if not db_order_detail:
        raise HTTPException(status_code=404, detail="OrderDetail not found")
    return db_order_detail