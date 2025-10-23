from typing import Generic, TypeVar, Optional, Any
from pydantic  import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
  status: str
  code: int
  message: Optional[str] = None
  data: Optional[T] = None

class ErrorDetail(BaseModel):
  field: Optional[str] = None
  message: str

class ErrorResponse(BaseModel):
  status: str
  code: int
  message: str
  errors: Optional[list[ErrorDetail]] = None

def success_response(data: Any = None, message: str = "Success", code: int = 200):
  return {
    "status" : "success",
    "code"   : code,
    "message" : message,
    "data" : data
  }

def error_response(message: str, code: int = 400, errors: list = None):
  response = {
      "status": "error",
      "code": code,
      "message": message
  }
  if errors:
      response["errors"] = errors
  return response