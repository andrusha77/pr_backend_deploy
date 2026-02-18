from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .db import get_db
from . import models
from .auth import decode_token
from jose import JWTError

security = HTTPBearer()

def get_current_user(
    cred: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(cred.credentials)
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(user=Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")
    return user
