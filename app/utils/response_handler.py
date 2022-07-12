from app.models.pydantic.response import BaseResponse


def success(code=200, data=None, message="successful!") -> BaseResponse:
    """Success Response Formatter

    Args:
        code (int, optional): Status Code. Defaults to 200.
        data (any, optional): Response Data. Defaults to None.
        message (str, optional): Informational Message. Defaults to "successful!".

    Returns:
        BaseResponse: Formatted Response
    """
    return {"code": code, "status": True, "data": data, "message": message}
