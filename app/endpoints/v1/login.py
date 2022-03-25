from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.routing import APIRouter
from authentication.jwt import generate_token_with_user_uuid

from authentication.jwt import jwt_encode
from database.Collections.UserInfo import create_user_by_phone, UserInfoPhone
from schemas.login import LoginRequest, LoginResponse

router = APIRouter()

@router.post(
    "/",
    response_model=LoginResponse,
)
def login_user(
    body: LoginRequest
):
    token = ""
    
    if body.phone:
        user: UserInfoPhone = UserInfoPhone.get_user_by_phone(body.phone)
        if not user:
            create_user_by_phone(body.phone)
            user: UserInfoPhone = UserInfoPhone.get_user_by_phone(body.phone)
        
        if body.otp:
            if user.submit_otp(body.otp):
                # Generate JWT token
                token = generate_token_with_user_uuid(user.uuid)
            else:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="Incorrect/Expired OTP."
                )
        else:
            user.create_new_otp()
            
            return {
                "message": "New OTP is genereted."
            }
    if body.email:
        # create_user_by_phone(body.email)
        pass
    if body.username and body.password:
        # create_user_by_phone(body.username, body.password)
        pass
    else:
        HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Incorrect Registeration Body."
        )
    
    return LoginResponse(
        token=token
    )