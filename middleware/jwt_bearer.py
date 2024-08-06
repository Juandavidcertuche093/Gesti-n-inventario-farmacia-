from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from config.database import get_db
from models.operator import Operario
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(Operario).filter(Operario.name == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_superuser(current_user: Operario = Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No hay suficientes permisos"
        )
    return current_user



# Con esta implementación, la autenticación básica (get_current_user) se utiliza para permitir que todos los usuarios autenticados accedan a la lista de medicamentos. Para las acciones más sensibles, como la eliminación de medicamentos, se utiliza get_current_active_superuser para restringir el acceso únicamente a los administradores