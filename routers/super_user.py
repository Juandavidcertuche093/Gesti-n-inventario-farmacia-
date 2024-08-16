import os
from fastapi import APIRouter
from schemas.super_user import User
from utils.jwt_manager import create_token
from fastapi.responses import JSONResponse
from fastapi import HTTPException

super_user_router = APIRouter()

admin_name = os.getenv("ADMIN_NAME")
admin_password = os.getenv("ADMIN_PASSWORD")


@super_user_router.post('/api/v1/auth/login', tags=['Auth_Super_user'])
def login_super_user(user: User):
    if user.name == admin_name and user.password == admin_password:
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content={'access_token': token})
    else:
        raise HTTPException(status_code=401, detail='Credenciales incorrectas')
    