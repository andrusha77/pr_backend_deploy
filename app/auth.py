from passlib.context import CryptContext
import hashlib

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
VERSION_MARK = "AUTH_V2_SHA256"

def _normalize_password(password: str) -> bytes:
    # перетворюємо в стабільні байти довжини 32 (sha256)
    return hashlib.sha256(password.encode("utf-8")).digest()

def hash_password(p: str) -> str:
    return pwd.hash(_normalize_password(p).hex())

def verify_password(p: str, h: str) -> bool:
    return pwd.verify(_normalize_password(p).hex(), h)

def create_token(user_id: int, is_admin: bool):
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "is_admin": is_admin, "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
