from fastapi import APIRouter, Path, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session

from schemas.medicine import UsuarioCreate, UsuarioBase
from services.users import UsersServices

users_router = APIRouter()

# ENDEPOINTS para los usuarios (rutas)

@users_router.get('/api/v1/users/list', tags=['Users'], response_model=list[UsuarioBase], status_code=200)
def get_users(db: Session = Depends(get_db)) -> list[UsuarioBase]:
    result = UsersServices(db).get_users()
    return result

@users_router.get('/api/v1/users/cedula/{cedula}', tags=['Users'], response_model=UsuarioBase, status_code=200)
def get_usurs_by_identificatiom(cedula: str = Path(..., min_length=5, max_length=11), db: Session = Depends(get_db)) -> UsuarioBase:
    result = UsersServices(db).get_users_by_identificatiom(cedula)
    if not result:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return result

@users_router.get('/api/v1/users/nombre/{nombre}', tags=['Users'], response_model=UsuarioBase, status_code=200)
def get_usurs_by_name(nombre: str = Path(..., title= 'Nombre del usuario'), db: Session = Depends(get_db)) -> UsuarioBase:
    result = UsersServices(db).get_users_by_name(nombre)
    if not result:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    return result

@users_router.post('/api/v1/users/record', tags=['Users'], response_model=UsuarioCreate, status_code=201)
def create_users(users: UsuarioCreate, db: Session = Depends(get_db)) ->dict:
    result = UsersServices(db).create_users(users)
    if not result:
        raise HTTPException(status_code=404, detail='Error al registrar el usuario')
    return result

@users_router.put('/api/v1/users/update/{cedula}', tags=['Users'], response_model=UsuarioBase, status_code=200)
def update_users(cedula: int, users: UsuarioBase, db: Session = Depends(get_db)) -> UsuarioBase:
    result = UsersServices(db).get_users_by_identificatiom(cedula)
    if not result:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    update_users = UsersServices(db).update_users(cedula, users)
    return update_users

@users_router.delete('/api/v1/users/delete/{cedula}', tags=['Users'], response_model=dict)
def delete_users(cedula: int, db: Session = Depends(get_db)) -> dict:
    result = UsersServices(db).get_users_by_identificatiom(cedula)
    if not result:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    delete_users = UsersServices(db).delete_users(cedula)
    if delete_users:
        return {'message': 'Usuario eliminado con éxito'}
    else:
        raise HTTPException(status_code=500, detail='Error al eliminar el Usuario')
   
