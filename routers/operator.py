from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi.responses import JSONResponse
from config.database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError

from schemas.operator import Operario, OperarioCreateRequest, OperarioUpdate, OperarioResponse, Operario_password
from services.operator import OperatorServicio
from utils.jwt_manager import create_token, validate_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/operator")


operator_router = APIRouter()

@operator_router.get('/api/v1/operator/list', tags=['Operator'], response_model=list[OperarioResponse], status_code=200)
def get_operator(db: Session = Depends(get_db)) -> list[OperarioResponse]:
    result = OperatorServicio(db).get_operator()
    return result

@operator_router.get('/api/v1/operator/id/{id}' ,tags=['Operator'], response_model=OperarioResponse, status_code=200)
def get_operator_by_id(id: int = Path(..., ge=1, le=10), db: Session = Depends(get_db)) -> Operario:
    result = OperatorServicio(db).get_operator_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail='Operario no encontrado')
    return result

@operator_router.get('/api/v1/operator/name/{name}' ,tags=['Operator'], response_model=OperarioResponse, status_code=200)
def get_operator_by_name(name: str = Path(..., title='Nombre operario'), db: Session = Depends(get_db)) -> Operario:
    result = OperatorServicio(db).get_operator_by_name(name)
    if not result:
        raise HTTPException(status_code=404, detail='Nombre de operario no encontrado')
    return result

@operator_router.get('/api/v1/auth/me', tags=['Operator'])
def get_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = validate_token(token)
        username: str = payload.get("sub")      
        email: str = payload.get("email")
        rol_id: str = payload.get("rol_id")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido") #"name": name
        return {"username": username, "email": email, "rol_id": rol_id }
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    

@operator_router.post('/api/v1/operator/record', tags=['Operator'], response_model=OperarioResponse, status_code=201)
def create_operator(operator: OperarioCreateRequest, db: Session = Depends(get_db)) -> dict:
    result = OperatorServicio(db).create_operator(operator)
    if not result:
        raise HTTPException(status_code=404, detail='Error al registrar operario')
    return result


@operator_router.post('/api/v1/auth/login/operator', tags=['Operator'])
def login(operario_password: Operario_password, db: Session = Depends(get_db)):
    operario_service = OperatorServicio(db)
    operario = operario_service.get_worker_by_name(operario_password.name)
    if operario and operario_service.verify_operator_credentials(operario_password.name, operario_password.password):
        token: str = create_token({"sub": operario_password.name, "email":operario.email, "rol_id":operario.role_id})
        return JSONResponse(status_code=200, content={"access_token": token, "message": "Inicio de sesión exitoso"})
    raise HTTPException(status_code=401, detail='Credenciales incorrectas')


@operator_router.put('/api/v1/operator/update/{name}', tags=['Operator'], response_model=OperarioUpdate, status_code=200)
def update_operator(name: str, operator: OperarioUpdate, db: Session = Depends(get_db)):
    result = OperatorServicio(db).get_operator_by_name(name)
    if not result:
        return JSONResponse(status_code=404, content={'message': 'Operaio no encontrado'})
    OperatorServicio(db).update_operator(name, operator)
    OperatorServicio(db).update_password(name, operator.password)
    token_data = {"name": name}  # Aquí puedes agregar más información si es necesario
    token = create_token(token_data)
    return JSONResponse(status_code=200, content={'message':'Se ha modificado el operario','access_token': token})
  

@operator_router.delete('/api/v1/operator/delete/{id}', tags=['Operator'], response_model=dict, status_code=200)
def delete_operator(id: int, db: Session = Depends(get_db)) -> dict:
    result = OperatorServicio(db).get_operator_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail='Operario no encontrado')
    delete_operator = OperatorServicio(db).delete_operador(id)
    if delete_operator:
        return {'message': 'Operario eliminado'}
    else:
        raise HTTPException(status_code=500, detail='Error al eliminar el medicamento')