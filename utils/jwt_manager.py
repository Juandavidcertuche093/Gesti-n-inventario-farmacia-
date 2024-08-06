from jwt import encode, decode, PyJWKError, DecodeError, ExpiredSignatureError, InvalidSignatureError
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
import os
import jwt


# Lee la clave secreta desde la variable de entorno
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")



def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=360)  # Token válido por 360 minutos (6 horas)
    to_encode.update({"exp": expire})
    token: str = encode(to_encode, key=SECRET_KEY, algorithm='HS256')
    return token

#funcion para valiar el token
def validate_token(token: str) ->  dict:
    data: dict = decode(token, key= SECRET_KEY, algorithms=['HS256'])
    return data

#funcion para veryficar el token
def verify_token(token: str) -> dict:
    try:
        data = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=403, detail='Token ha expirado')
    except InvalidSignatureError:
        raise HTTPException(status_code=403, detail='Firma del token no válida')
    except DecodeError:
        raise HTTPException(status_code=403, detail='Token mal formado')
    except PyJWKError as e:
        raise HTTPException(status_code=403, detail=f'Error de verificación del token: {e}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error al decodificar el token: {e}')