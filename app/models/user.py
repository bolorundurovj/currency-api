from sqlalchemy import Boolean, Integer, String, Column
from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(256), nullable=True)
    email = Column(String(256), index=True, nullable=False)
    password = Column(String(256), nullable=False)
    is_disabled = Column(Boolean, default=False, nullable=False)
