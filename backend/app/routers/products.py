import os, shutil
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..deps import require_admin

router = APIRouter(prefix="/products", tags=["products"])
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("", response_model=list[schemas.ProductOut])
def all_products(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.id.desc()).all()

@router.get("/{pid}", response_model=schemas.ProductOut)
def one(pid: int, db: Session = Depends(get_db)):
    p = db.query(models.Product).filter(models.Product.id == pid).first()
    if not p: raise HTTPException(404, "Not found")
    return p

@router.post("", response_model=schemas.ProductOut)
def create(data: schemas.ProductCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    p = models.Product(**data.dict())
    db.add(p); db.commit(); db.refresh(p)
    return p

@router.post("/{pid}/image")
def upload_image(pid: int, file: UploadFile = File(...), db: Session = Depends(get_db), _=Depends(require_admin)):
    p = db.query(models.Product).filter(models.Product.id == pid).first()
    if not p: raise HTTPException(404, "Not found")

    ext = os.path.splitext(file.filename)[1].lower() or ".jpg"
    filename = f"product_{pid}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    p.image_url = f"/static/{filename}"
    db.commit()
    return {"imageUrl": p.image_url}
