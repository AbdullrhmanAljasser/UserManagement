from fastapi import FastAPI, Depends

from app.endpoints.v1 import login, register


app = FastAPI(

)

app.include_router(
    login.router,
    prefix="/login"
)


app.include_router(
    register.router,
    prefix="/register"
)