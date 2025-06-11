from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ErrorResponse(BaseModel):
    detail: str

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None