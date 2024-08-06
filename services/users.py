from models.medicine import Usuario as ModelUsers
from schemas.medicine import UsuarioCreate, UsuarioBase

class UsersServices():

    def __init__(self, db) -> None:
        self.db = db

    def get_users(self):
       result = self.db.query(ModelUsers).all()
       return result
        
    def get_users_by_identificatiom(self, cedula):
        result = self.db.query(ModelUsers).filter(ModelUsers.cedula == cedula).first()
        return result
        
    def get_users_by_name(self, nombre):
        result = self.db.query(ModelUsers).filter(ModelUsers.nombre == nombre).first()
        return result
    
    def create_users(self, usuarios: UsuarioCreate):
        new_user = ModelUsers(**usuarios.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)  # Refrescar el objeto para obtener cualquier valor generado por la base de datos
        return new_user

    def update_users(self, cedula: str, data: UsuarioBase):
        users = self.db.query(ModelUsers).filter(ModelUsers.cedula == cedula).first()
        if users:
            if hasattr(data, 'nombre'):
                users.nombre = data.nombre
            if hasattr(data, 'apellidos'):
                users.apellidos = data.apellidos
            if hasattr(data, 'telefono'):
                users.telefono = data.telefono
            if hasattr(data, 'email'):
                users.email = data.email
            self.db.commit()
            self.db.refresh(users)
        return users

    def delete_users(self, cedula: str) -> bool:
        self.db.query(ModelUsers).filter(ModelUsers.cedula == cedula).delete()
        self.db.commit()
        return True # Indicador de éxito
    