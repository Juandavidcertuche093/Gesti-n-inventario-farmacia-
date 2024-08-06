from models.medicine import Medicamento as ModelMedic
from schemas.medicine import MedicamentoCreate, MedicamentoBase

class MedicineService():

    def __init__(self, db) -> None:
        self.db = db
    
    def get_medicine(self):
        result = self.db.query(ModelMedic).all()
        return result
    
    def get_medicine_by_id(self, idMedicamento):
        result = self.db.query(ModelMedic).filter(ModelMedic.idMedicamento == idMedicamento).first()
        return result
    
    def get_medicine_by_name(self, nombreMed):
        result = self.db.query(ModelMedic).filter(ModelMedic.nombreMed == nombreMed).first()
        return result
    
    def create_medicine(self, medicine: MedicamentoCreate):
        new_medicine = ModelMedic (**medicine.model_dump())
        self.db.add(new_medicine)
        self.db.commit()
        self.db.refresh(new_medicine) # Esto refresca el objeto con los datos de la base de datos
        return new_medicine # Devolver el objeto creado
    
    def update_medicine(self, idMedicamento: int, data: MedicamentoBase):
        medicine = self.db.query(ModelMedic).filter(ModelMedic.idMedicamento == idMedicamento).first()
        if medicine:
            if hasattr(data, 'nombreMed'):
                medicine.nombreMed = data.nombreMed
            if hasattr(data, 'empaqueMed'):
                medicine.empaqueMed = data.empaqueMed
            if hasattr(data, 'unidadPorEmpaque'):
                medicine.unidadPorEmpaque = data.unidadPorEmpaque
            if hasattr(data, 'cantidadMed'):
                medicine.cantidadMed = data.cantidadMed
            if hasattr(data, 'presentacionMed'):
                medicine.presentacionMed = data.presentacionMed
            if hasattr(data, 'fechaVencimientoMed'):
                medicine.fechaVencimientoMed = data.fechaVencimientoMed
            if hasattr(data, 'especificacionMed'):
                medicine.especificacionMed = data.especificacionMed
            if hasattr(data, 'precioUnidad'):
                medicine.precioUnidad = data.precioUnidad
            if hasattr(data, 'precioCaja'):
                medicine.precioCaja = data.precioCaja
            self.db.commit()
            self.db.refresh(medicine)# Refresca el objeto desde la base de datos
        return medicine

    def delete_medicine(self, idMedicamento: int) -> bool:
        self.db.query(ModelMedic).filter(ModelMedic.idMedicamento == idMedicamento).delete()
        self.db.commit()
        return True #indeicador de exito
        