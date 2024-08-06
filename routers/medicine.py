from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from config.database import get_db
from sqlalchemy.orm import Session

from middleware.jwt_bearer import get_current_active_superuser, get_current_user
from models.operator import Operario
from schemas.medicine import Medicamento, MedicamentoBase, MedicamentoCreate
from services.medicine import MedicineService

medicine_router = APIRouter()

@medicine_router.get('/api/v1/medicine/list', tags=['Medicine'], response_model=list[MedicamentoBase], status_code=200) # , current_user: Operario = Depends(get_current_user)
def get_medicine(db: Session = Depends(get_db)) -> list[MedicamentoBase]:
    result = MedicineService(db).get_medicine()
    return result

@medicine_router.get('/api/v1/medicine/info/idMedicine/{idMedicamento}', tags=['Medicine'], response_model=MedicamentoBase, status_code=200)
def get_medicine_by_id(idMedicamento: int = Path(..., ge=1, le=20000), db: Session = Depends(get_db)) -> MedicamentoBase:
    result = MedicineService(db).get_medicine_by_id(idMedicamento)
    if not result:
        raise HTTPException(status_code=404, detail='Medicamento no encontrado')
    return result

@medicine_router.get('/api/v1/medicine/info/nombreMed/{nombreMed}', tags=['Medicine'], response_model=MedicamentoBase)
def get_medicine_by_name(nombreMed: str = Path(..., title='Nombre del medicamento'), db: Session = Depends(get_db)) -> Medicamento:
    result = MedicineService(db).get_medicine_by_name(nombreMed)
    if not result:
        raise HTTPException(status_code=404, detail='Nombre del medicamento no encontrado')
    return result

@medicine_router.post('/api/v1/medicine/record', tags=['Medicine'], response_model=MedicamentoCreate, status_code=201)
def create_medicine(medicine: MedicamentoCreate, db: Session = Depends(get_db)) -> dict:
    result = MedicineService(db).create_medicine(medicine)
    if not result:
        raise HTTPException(status_code=404, detail='Error al registrar el medicamento')
    return result


@medicine_router.put('/api/v1/medicine/update/idMedicamento/{idMedicamento}', tags=['Medicine'], response_model=MedicamentoBase, status_code=200)
def update_medicine(idMedicamento: int, medicine: MedicamentoBase, db: Session = Depends(get_db)) -> MedicamentoBase:
    result = MedicineService(db).get_medicine_by_id(idMedicamento)
    if not result:
        raise HTTPException (status_code=404, detail='Medicamento no encontrado')
    update_medicine = MedicineService(db).update_medicine(idMedicamento, medicine)
    return update_medicine


@medicine_router.delete('/api/v1/medicine/delete/{idMedicamento}', tags=['Medicine'], response_model=dict)
def delete_medicine(idMedicamento: int, db: Session = Depends(get_db), ) -> dict: #current_user: Operario = Depends(get_current_active_superuser)
    result = MedicineService(db).get_medicine_by_id(idMedicamento)
    if not result:
        raise HTTPException(status_code=404, detail='Medicamento no encontrado')
    delete_success = MedicineService(db).delete_medicine(idMedicamento)
    if delete_success:
        return {'message': 'Medicamento eliminado con éxito'}
    else:
        raise HTTPException(status_code=500, detail='Error al eliminar el medicamento')