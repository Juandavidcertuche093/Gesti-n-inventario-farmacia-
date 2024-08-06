from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Operario(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=5, max_length=70)
    email: EmailStr
    password: str = Field(min_length=5)
    role_id: int

class OperarioCreateRequest(BaseModel):
    name: str = Field(min_length=5, max_length=70)
    email: EmailStr
    password: str = Field(min_length=5)
    role_id: int

class OperarioUpdate(BaseModel):
    name: str
    password: str
    email: EmailStr

class OperarioResponse(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
    role_id: int

class Operario_password(BaseModel):    
    id: Optional[str] = None
    name: str    
    password: str