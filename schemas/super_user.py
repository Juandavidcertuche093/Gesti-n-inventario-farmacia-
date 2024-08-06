from pydantic import BaseModel

# se crea una clase para el super Usuario y contraseña
class User(BaseModel):
    name:str
    password:str