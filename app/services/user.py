from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.pydantic.user import UserCreate, UserInDBBase
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

db = SessionLocal()
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get(id: str, db: Session = db) -> User:
    """
    Retrieve Single User By ID
    :param id: User ID
    :param db: Db Session
    :return: User
    """
    return db.query(User).filter(User.id == id).first()


async def get_by_email(email: str, db: Session = db) -> User:
    """
    Retrieve Single User By Email
    :param email: User Email
    :param db: Db Session
    :return: User
    """
    return db.query(User).filter(User.email == email).first()


async def create(user: UserCreate, db: Session = db) -> UserInDBBase:
    """
    Create and Save a user
    :param user: User Object
    :param db: Db Session
    :return: User
    """
    obj_in_data = jsonable_encoder(user)
    obj_in_data["password"] = await get_password_hash(obj_in_data.get("password"))
    db_obj = User(**obj_in_data)  # type: ignore
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return {
        "id": db_obj.id,
        "email": db_obj.email,
        "full_name": db_obj.full_name,
    }


async def get_password_hash(password: str) -> str:
    """
    Hash password
    :param password: Plain password
    :return: Hashed password
    """
    return PWD_CONTEXT.hash(password)
