from typing import Optional

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: Optional[str]
    password: Optional[str]
    
    phone: Optional[str]
    
    email: Optional[str]

    otp: Optional[str]

class LoginResponse(BaseModel):
    token: Optional[str]
    message: Optional[str]
    