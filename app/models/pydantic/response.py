from typing import Generic, TypeVar, Union
from pydantic.generics import GenericModel


DataType = TypeVar("DataType")


class BaseResponse(GenericModel, Generic[DataType]):
    status: bool
    message: Union[str, None]
    code: int
    data: DataType
