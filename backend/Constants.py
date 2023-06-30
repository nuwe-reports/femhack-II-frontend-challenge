from enum import Enum
from pydantic import BaseModel 

class HttpErrors(Enum):
    NOT_FOUND = 404 
    INTERNAL_SERVER_ERROR = 500
    BAD_REQUEST = 400

class ErrorResponseModel(BaseModel):
    Detail: str
    Errors: dict= {}

class CountryData(BaseModel):
    internet_users_percentatge: int 
    internet_users_number: int 

class ResponseModel(BaseModel):
    Message: str

class Countries(ResponseModel):
    Countries: list | None

class CountryDataPerModel(ResponseModel):
    Data: dict  = {}
