from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import require_admin
from .. import models

router = APIRouter(prefix="/admin/debug", tags=["debug"])

@router.get("/users")
def debug_users(db: Session = Depends(get_db), _=Depends(require_admin)):
    users = db.query(models.User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "is_admin": u.is_admin
        }
        for u in users
    ]

@router.get("/products")
def debug_products(db: Session = Depends(get_db), _=Depends(require_admin)):
    products = db.query(models.Product).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "price": float(p.price),
            "image_id": p.image_id
        }
        for p in products
    ]

@router.get("/orders")
def debug_orders(db: Session = Depends(get_db), _=Depends(require_admin)):
    orders = db.query(models.Order).all()
    return [
        {
            "id": o.id,
            "user_id": o.user_id,
            "total": float(o.total),
            "status": o.status
        }
        for o in orders
    ]
from fastapi import HTTPException

@router.post("/bootstrap-admin/{username}")
def bootstrap_admin(username: str, db: Session = Depends(get_db)):
    # 1) якщо адмін вже існує — не даємо
    admin_exists = db.query(models.User).filter(models.User.is_admin == True).first()
    if admin_exists:
        raise HTTPException(status_code=403, detail="Admin already exists")

    # 2) шукаємо користувача
    u = db.query(models.User).filter(models.User.username == username).first()
    if not u:
        raise HTTPException(status_code=404, detail="User not found")

    # 3) робимо адміном
    u.is_admin = True
    db.commit()
    return {"ok": True, "username": u.username, "is_admin": u.is_admin}
