from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    email: str
    password: str
    full_name: Optional[str]


class UserInDBBase(BaseModel):
    id: int
    full_name: Optional[str]
    email: str


class UserAuth(BaseModel):
    access_token: str
    token_type: str
