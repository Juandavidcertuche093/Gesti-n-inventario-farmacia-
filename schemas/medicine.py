from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import date

# Usuario
class UsuarioBase(BaseModel):
    cedula: int
    nombre: str
    apellidos: str
    telefono: int
    email: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    cedula: int
    notificaciones: List["Notificacion"] = []
    facturas: List["Factura"] = []

    class Config:
        orm_mode = True


# Notificacion
class NotificacionBase(BaseModel):
    descripcionNot: str
    fechaNot: date
    Usuario_cedula: int

class NotificacionCreate(NotificacionBase):
    pass

class Notificacion(NotificacionBase):
    idNotificacion: int

    class Config:
        orm_mode = True


# Medicamento
class MedicamentoBase(BaseModel):
    idMedicamento: int
    nombreMed: str
    empaqueMed: str
    unidadPorEmpaque: int
    cantidadMed: int
    presentacionMed: str
    fechaVencimientoMed: date
    especificacionMed: str
    precioUnidad: float
    precioCaja: float

class MedicamentoCreate(MedicamentoBase):
    pass

class Medicamento(MedicamentoBase):
    idMedicamento: int
    detalles_factura: List["FacturaDetalle"] = []

    class Config:
        orm_mode = True


# FacturaDetalle
class FacturaDetalleBase(BaseModel):
    medicamento_id: int
    cantidad: int
    precio_unitario: float
    tipo_venta: str

    @validator('tipo_venta')
    def check_tipo_venta(cls, v):
        if v not in ('unidad', 'caja'):
            raise ValueError('El tipo de venta debe ser "unidad" o "caja"')
        return v
    

class FacturaDetalleCreate(FacturaDetalleBase):
    pass

class FacturaDetalle(FacturaDetalleBase):
    id: int
    precio_total: float

    class Config:
        orm_mode = True


#Factura
class FacturaBase(BaseModel):
    fechafactura: date
    Usuario_cedula: int
    detalles: List[FacturaDetalleCreate]

class FacturaCreate(FacturaBase):
    pass

class Factura(FacturaBase):
    idfactura: int
    detalles: List[FacturaDetalle]

    class Config:
        orm_mode = True
