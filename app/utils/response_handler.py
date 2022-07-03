from app.models.pydantic.response import BaseResponse


def success(code=200, data=None) -> BaseResponse:
    return {"code": code, "status": True, "data": data}
