from http import HTTPStatus

from fastapi import HTTPException
from fastapi.routing import APIRouter

from database.session import db_client
from database.Collections.UserInfo import create_user_by_phone
from schemas.register import RegisterRequest, RegisterResponse

router = APIRouter()

@router.post(
    "/",
    response_model=RegisterResponse
)
def register_user(
    body: RegisterRequest
):
    if body.username and body.password:
        # create_user_by_phone(body.username, body.password)
        pass
    else:
        HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Incorrect Registeration Body."
        )
    
    return RegisterResponse(
        msg="Successful Registeration!"
    )