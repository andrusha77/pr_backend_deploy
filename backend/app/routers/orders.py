from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..deps import get_current_user, require_admin

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/my", response_model=list[schemas.OrderOut])
def my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Order).filter(models.Order.user_id == user.id).order_by(models.Order.id.desc()).all()

@router.post("")
def create_order(data: schemas.CreateOrderIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not data.items:
        raise HTTPException(400, "Empty items")

    order = models.Order(user_id=user.id, status="New", comment=data.comment)
    db.add(order); db.commit(); db.refresh(order)

    total = 0
    for it in data.items:
        p = db.query(models.Product).filter(models.Product.id == it.product_id).first()
        if not p: raise HTTPException(404, f"Product {it.product_id} not found")
        if it.quantity <= 0: raise HTTPException(400, "Bad quantity")

        total += float(p.price) * it.quantity
        db.add(models.OrderItem(
            order_id=order.id,
            product_id=p.id,
            title_snapshot=p.title,
            price_snapshot=p.price,
            quantity=it.quantity
        ))

    order.total = total
    db.commit()
    return {"id": order.id}

@router.post("/admin/{user_id}")
def admin_create(user_id: int, data: schemas.CreateOrderIn, db: Session = Depends(get_db), _=Depends(require_admin)):
    if not data.items:
        raise HTTPException(400, "Empty items")

    u = db.query(models.User).filter(models.User.id == user_id).first()
    if not u: raise HTTPException(404, "User not found")

    order = models.Order(user_id=user_id, status="New", comment=data.comment)
    db.add(order); db.commit(); db.refresh(order)

    total = 0
    for it in data.items:
        p = db.query(models.Product).filter(models.Product.id == it.product_id).first()
        if not p: raise HTTPException(404, "Product not found")
        total += float(p.price) * it.quantity
        db.add(models.OrderItem(
            order_id=order.id,
            product_id=p.id,
            title_snapshot=p.title,
            price_snapshot=p.price,
            quantity=it.quantity
        ))
    order.total = total
    db.commit()
    return {"id": order.id}
