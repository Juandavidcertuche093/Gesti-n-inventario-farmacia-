from sqlalchemy import CheckConstraint, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    cedula = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(30))
    apellidos = Column(String(30))
    telefono = Column(String(20))
    email = Column(String(45))
    
    notificaciones = relationship("Notificacion", back_populates="usuario")
    facturas = relationship("Factura", back_populates="usuario")


class Notificacion(Base):
    __tablename__ = 'notificacion'
    
    idNotificacion = Column(Integer, primary_key=True, index=True)
    descripcionNot = Column(String(200))
    fechaNot = Column(Date)
    Usuario_cedula = Column(Integer, ForeignKey('usuario.cedula'))
    
    usuario = relationship("Usuario", back_populates="notificaciones")


class Medicamento(Base):
    __tablename__ = 'medicamento'
    
    idMedicamento = Column(Integer, primary_key=True, index=True)
    nombreMed = Column(String(50))
    empaqueMed = Column(String(20))  # Ej: "Caja"
    unidadPorEmpaque = Column(Integer)  # Ej: 30 (tabletas por caja)
    cantidadMed = Column(Integer)  # Total de tabletas disponibles
    presentacionMed = Column(String(15))  # Ej: "Tableta"
    fechaVencimientoMed = Column(Date)
    especificacionMed = Column(String(100))  # Ej: "500mg"
    precioUnidad = Column(Float)  # Precio por unidad (tableta)
    precioCaja = Column(Float)  # Precio por caja
    
    detalles_factura = relationship("FacturaDetalle", back_populates="medicamento")

class Factura(Base):
    __tablename__ = 'factura'
    
    idfactura = Column(Integer, primary_key=True, index=True)
    fechafactura = Column(Date)
    Usuario_cedula = Column(Integer, ForeignKey('usuario.cedula'))
    
    usuario = relationship("Usuario", back_populates="facturas")
    detalles = relationship("FacturaDetalle", back_populates="factura", cascade="all, delete-orphan")


class FacturaDetalle(Base):
    __tablename__ = 'factura_detalle'
    
    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey('factura.idfactura'))
    medicamento_id = Column(Integer, ForeignKey('medicamento.idMedicamento'))
    cantidad = Column(Integer)    
    precio_unitario = Column(Float)
    precio_total = Column(Float)
    tipo_venta = Column(String(20),  nullable=False)  # Nuevo campo para tipo de venta (unidad o caja)

    # Restricción CHECK para asegurar que tipo_venta sea "unidad" o "caja"
    __table_args__ = (
        CheckConstraint("tipo_venta IN ('unidad', 'caja')", name='check_tipo_venta'),
    )
    
    
    factura = relationship("Factura", back_populates="detalles")
    medicamento = relationship("Medicamento", back_populates="detalles_factura")
