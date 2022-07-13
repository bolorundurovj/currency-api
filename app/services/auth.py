from typing import Optional, Union
from datetime import datetime, timedelta
from sqlalchemy.orm.session import Session
from jose import jwt
from app.db.session import SessionLocal
from app.models.pydantic.user import UserInDBBase
from app.models.user import User
from passlib.context import CryptContext
from app.utils.configuration import Config
from app.utils.error_handler import OpsException

config = Config()

db = SessionLocal()


async def authenticate(email: str, password: str, db: Session = db) -> Union[UserInDBBase, None]:
    """Authenticates a user

    Args:
        email (str): User's email addres
        password (str):  User's password
        db (Session, optional): Database session. Defaults to db.

    Returns:
        Union[UserInDBBase, None]: User Object
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not await verify_password(password, user.password):
        return None
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
    }


async def create_access_token(sub: UserInDBBase) -> str:
    """Generate JWT

    Args:
        sub (UserInDBBase): User Subject

    Returns:
        str: JWT
    """
    response = await _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=int(config.token_validity_period)),
        sub=sub,
    )
    return response


async def _create_token(token_type: str, lifetime: timedelta, sub: UserInDBBase) -> str:
    """Encode data into JWT

    Args:
        token_type (str): Token Type
        lifetime (timedelta): Expiry Period
        sub (UserInDBBase): User Subject

    Returns:
        str: JWT
    """

    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = sub
    return jwt.encode(payload, config.jwt_secret, algorithm=config.hash_algorithm)


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares plain password to hashed password

    Args:
        plain_password (str): Plain password
        hashed_password (str): Hashed password

    Returns:
        bool: boolean
    """

    return PWD_CONTEXT.verify(plain_password, hashed_password)
