from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

from config.cors_config import origins
from config.database import Base, engine, SessionLocal
from models.operator import Role, Operario
from routers.medicine import medicine_router
from routers.operator import operator_router
from routers.users import users_router
from routers.super_user import super_user_router
from routers.billing import factura_router

app = FastAPI()
app.title = 'API de gestión de inventario de farmacia'
app.version = '0.1'

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(medicine_router)
app.include_router(operator_router)
app.include_router(users_router)
app.include_router(super_user_router)
app.include_router(factura_router)


def init_db():
    db = SessionLocal(bind=engine)
    
    # Crear roles
    if not db.query(Role).first():  # Evitar duplicados
        admin_role = Role(name="admin")
        user_role = Role(name="oper")
        db.add(admin_role)
        db.add(user_role)
        db.commit()

    # Crear superusuario
    admin_name = os.getenv("ADMIN_NAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_email = os.getenv("ADMIN_EMAIL")
    
    if not db.query(Operario).filter(Operario.name == admin_name).first():
        superuser = Operario(name=admin_name, email=admin_email, password_hash=admin_password, role_id=admin_role.id)
        db.add(superuser)
        db.commit()

init_db()
