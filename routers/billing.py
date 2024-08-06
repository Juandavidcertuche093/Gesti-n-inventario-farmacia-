from fastapi import APIRouter, Path, Depends, HTTPException
from schemas.medicine import Factura, FacturaCreate, FacturaBase
from sqlalchemy.orm import Session
from config.database import get_db
from services.billing import FacturaService



factura_router = APIRouter()

@factura_router.get('/api/v1/facturas/list', tags=['Facturacion'], response_model=list[Factura], status_code=200)
def get_factura(db: Session = Depends(get_db)) -> list[Factura]:
    result = FacturaService(db).get_factura()
    return result

@factura_router.get('/api/v1/factiras/info/id/{idFactura}', tags=['Facturacion'], response_model=FacturaBase, status_code=200)
def get_factura_by_id(idFactura: int = Path(..., ge=1, le=20000), db: Session = Depends(get_db)) -> FacturaBase:
    result = FacturaService(db).get_factura_by_id(idFactura)
    if not result:
        raise HTTPException(status_code=404, detail='Factura no encontrada')
    return result

@factura_router.post('/api/v1/facturas/create', tags=['Facturacion'], response_model= Factura, status_code=201)
def create_factura(factura: FacturaCreate, db: Session = Depends(get_db)) -> Factura:
    try:
        result = FacturaService(db).create_Factura(factura)
    except HTTPException as e:
        raise e
    return result

@factura_router.delete('/api/v1/facturas/delete/id/{idFactura}', tags=['Facturacion'], response_model=dict)
def delete_factura(idFactura: int, db: Session = Depends(get_db)) -> dict:
    result = FacturaService(db).get_factura_by_id(idFactura)
    if not result:
        raise HTTPException(status_code=404, detail='Factura no encontrada')
    delete_factura = FacturaService(db).delete_factura(idFactura)
    if delete_factura:
        return{'message': 'Factura Eliminada con exito'}
    else:
        raise HTTPException(status_code=500, detail='Error al eliminar la factura')
