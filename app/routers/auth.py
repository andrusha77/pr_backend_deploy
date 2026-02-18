from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..auth import hash_password, verify_password, create_token
from ..auth import VERSION_MARK


router = APIRouter(prefix="/auth", tags=["auth"])
@router.post("/register")
def register(data: schemas.RegisterIn, db: Session = Depends(get_db)):
    if len(data.username) < 3 or len(data.password) < 4:
        raise HTTPException(400, "Weak credentials")

    exists = db.query(models.User).filter(models.User.username == data.username).first()
    if exists:
        raise HTTPException(400, "Username already exists")
    pwd_bytes = data.password.encode("utf-8")
    if len(pwd_bytes) > 200:
        raise HTTPException(status_code=400, detail="Password too long")
    print("AUTH VERSION:", VERSION_MARK, "pw_len_bytes:", len(data.password.encode("utf-8")))
    user = models.User(username=data.username, password_hash=hash_password(data.password), is_admin=False)
    db.add(user); db.commit(); db.refresh(user)
    return {"ok": True}

@router.post("/login", response_model=schemas.AuthOut)
def login(data: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_token(user.id, user.is_admin)
    return {"token": token, "user": user}
