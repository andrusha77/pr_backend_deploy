from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models
from ..deps import require_admin

router = APIRouter(tags=["images"])

MAX_BYTES = 2 * 1024 * 1024  # 2MB ліміт щоб не вбити free базу

@router.get("/images/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    img = db.query(models.Image).filter(models.Image.id == image_id).first()
    if not img:
        raise HTTPException(404, "Image not found")
    return Response(content=img.data, media_type=img.content_type)

@router.post("/products/{pid}/image")
async def upload_product_image(
    pid: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    p = db.query(models.Product).filter(models.Product.id == pid).first()
    if not p:
        raise HTTPException(404, "Product not found")

    data = await file.read()
    if len(data) == 0:
        raise HTTPException(400, "Empty file")
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "Image too large (max 2MB)")

    content_type = file.content_type or "image/jpeg"
    if not content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")

    # якщо у товару вже є картинка — оновимо її (щоб не плодити записи)
    if p.image_id:
        img = db.query(models.Image).filter(models.Image.id == p.image_id).first()
        if img:
            img.data = data
            img.content_type = content_type
            db.commit()
            return {"imageId": img.id, "imageUrl": f"/images/{img.id}"}

    img = models.Image(data=data, content_type=content_type)
    db.add(img)
    db.commit()
    db.refresh(img)

    p.image_id = img.id
    db.commit()

    return {"imageId": img.id, "imageUrl": f"/images/{img.id}"}
