from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
# from pydantic.generics import GenericModel

GenericModel = BaseModel

T = TypeVar('T')


class BookSchema(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True  # was `orm_mode = True` in Pydantic v1


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestBook(BaseModel):
    parameter: BookSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]