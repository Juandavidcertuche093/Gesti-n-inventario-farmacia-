from typing import Optional
import bcrypt
from models.operator import Operario as OperatorModel
from schemas.operator import Operario

class OperatorServicio():

    def __init__(self, db) -> None:
        self.db = db
    
    def get_operator(self):
        result = self.db.query(OperatorModel).all()
        return result
    
    def create_operator(self, operator: Operario) -> OperatorModel:
        """
        Crea un nuevo operario con la información proporcionada y lo guarda en la base de datos.

        """
        password_hash = self.hash_password(operator.password)
        new_operator = OperatorModel(
            name=operator.name,
            email=operator.email,
            password_hash=password_hash,
            role_id=operator.role_id
        )
        self.db.add(new_operator)
        self.db.commit()
        self.db.refresh(new_operator)# Refresca la instancia para obtener el ID generado
        return new_operator
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash seguro para la contraseña proporcionada.

        """
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hash_password.decode('utf-8')
    
    def verify_operator_credentials(self, name: str, password: str) -> bool:
        """
        Verifica si las credenciales del operario (nombre y contraseña) son correctas.

        """
        users = self.get_operator_by_name(name)
        if users and bcrypt.checkpw(password.encode('utf-8'), users.password_hash.encode('utf-8')):
            return True
        return False
    
    def get_worker_by_name(self, name: str) -> Optional[OperatorModel]:
        """
        Recupera un operador de la base de datos utilizando su nombre.
        
        """
        return self.db.query(OperatorModel).filter_by(name=name).first()
    


    def get_operator_by_id(self, id):
        result = self.db.query(OperatorModel).filter(OperatorModel.id == id).first()
        return result
    
    def get_operator_by_name(self, name):
        result = self.db.query(OperatorModel).filter(OperatorModel.name == name).first()
        return result
    
    def update_operator(self, name: str, data: OperatorModel):
        operator = self.db.query(OperatorModel).filter(OperatorModel.name == name).first()
        if operator:
            if hasattr(data, 'name'):
                    operator.name = data.name
            if hasattr(data, 'email'):
                    operator.email = data.email  
            if hasattr(data, 'password_hash'):
                    operator.password_hash = data.password_hash
            self.db.commit()
            self.db.refresh(operator) # Refresca el objeto desde la base de datos
        return operator
    
    def update_password(self, name: str, new_password: str):
        # optenemoes el operdaro por su nombre
        operator = self.get_operator_by_name(name)
        if operator:
            hashed_password = self.hash_password(new_password)
            operator.password_hash = hashed_password
            self.db.commit()
        return
    
    def delete_operador(self, id: int):
        self.db.query(OperatorModel).filter(OperatorModel.id == id).delete()
        self.db.commit()
        return True  # Indicador de éxit
    


        
         




         
         