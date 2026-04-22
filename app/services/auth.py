from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import User

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def ensure_admin_user(db: Session) -> User:
    user = db.query(User).filter(User.email == settings.admin_email).first()
    if user:
        return user

    user = User(email=settings.admin_email, password_hash=hash_password(settings.admin_password), is_active=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
