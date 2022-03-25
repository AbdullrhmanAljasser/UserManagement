from typing import Optional

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: Optional[str]
    password: Optional[str]
    
class RegisterResponse(BaseModel):
    msg: str