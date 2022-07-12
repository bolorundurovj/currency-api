from typing import Any
from fastapi import APIRouter, Depends
from app.models.pydantic.user import UserAuth, UserCreate, UserBase, UserInDBBase
from app.services import auth, user as user_service
from app.utils.dependencies import has_access
from app.utils.error_handler import OpsException
from app.models.pydantic.response import BaseResponse
from app.utils.helpers import is_valid_email
from app.utils.response_handler import success


PROTECTED = [Depends(has_access)]


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=BaseResponse[UserAuth])
async def login(request: UserBase) -> Any:
    user = await auth.authenticate(email=request.email, password=request.password)
    if not user:
        raise OpsException(code=400, message="Incorrect username or password")

    return success(
        data={
            "access_token": await auth.create_access_token(sub=user),
            "token_type": "bearer",
        }
    )


@router.post("/signup", response_model=BaseResponse[UserInDBBase], status_code=201)
async def create_user_signup(user_data: UserCreate):
    if not is_valid_email(user_data.email):
        raise OpsException(code=400, message="Email is not valid")
    user = await user_service.get_by_email(email=user_data.email)
    if user:
        raise OpsException(
            code=400,
            message="The user with this email already exists in the system",
        )
    response = await user_service.create(user=user_data)
    return success(code=201, data=response)
