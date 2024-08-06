
from fastapi import HTTPException
from schemas.medicine import FacturaCreate
from models.medicine import Factura as ModelFactura
from models.medicine import Medicamento as ModelMedic
from models.medicine import FacturaDetalle as ModelFacturaDetalle


class FacturaService():

    def __init__(self, db) -> None:
        self.db = db
    
    def get_factura(self):
        result = self.db.query(ModelFactura).all()
        return result
    
        
    def get_factura_by_id(self, idFactura):        
        result = self.db.query(ModelFactura).filter(ModelFactura.idfactura == idFactura).first()
        return result
    

    def delete_factura(self, idFactura: int):
        # Obtener todos los detalles de la factura
        detalles = self.db.query(ModelFacturaDetalle).filter(ModelFacturaDetalle.factura_id == idFactura).all()
        for detalle in detalles:
            self.db.delete(detalle)
        # Eliminar la factura después de eliminar los detalles
        factura = self.db.query(ModelFactura).filter(ModelFactura.idfactura == idFactura).first()
        if factura:
            self.db.delete(factura)
            self.db.commit()
            return True
        return False
    
    def create_Factura(self, factura_data: FacturaCreate):
    # Crear factura
        new_factura = ModelFactura(
            fechafactura=factura_data.fechafactura,
            Usuario_cedula=factura_data.Usuario_cedula
        )
        self.db.add(new_factura)
        self.db.commit()
        self.db.refresh(new_factura)

        # Crear los detalles de la facturación y actualizar el stock
        for detalle in factura_data.detalles:
            medicamento = self.db.query(ModelMedic).filter(ModelMedic.idMedicamento == detalle.medicamento_id).first()
            if medicamento:
                # Verificar si se vende por unidad o por empaque
                if detalle.tipo_venta == 'unidad':
                    if medicamento.cantidadMed < detalle.cantidad:
                        raise HTTPException(status_code=400, detail=f"Stock insuficiente para el medicamento ID: {detalle.medicamento_id}")

                    # Actualizar stock de unidades disponibles
                    medicamento.cantidadMed -= detalle.cantidad
                    
                    # Calcular precio total basado en precio por unidad
                    precio_total = detalle.cantidad * medicamento.precioUnidad

                    # Crear detalle de factura
                    new_detalle = ModelFacturaDetalle(
                        factura_id=new_factura.idfactura,
                        medicamento_id=detalle.medicamento_id,
                        cantidad=detalle.cantidad,
                        precio_unitario=medicamento.precioUnidad,
                        precio_total=precio_total,
                        tipo_venta='unidad'  # Asegúrate de asignar correctamente este campo
                    )
                elif detalle.tipo_venta == 'caja':
                    # Total de unidades requeridas
                    unidades_requeridas = detalle.cantidad * medicamento.unidadPorEmpaque
                    
                    if medicamento.cantidadMed < unidades_requeridas:
                        raise HTTPException(status_code=400, detail=f"Stock insuficiente para el medicamento ID: {detalle.medicamento_id}")

                    # Actualizar stock de unidades disponibles
                    medicamento.cantidadMed -= unidades_requeridas
                    
                    # Calcular precio total basado en precio por caja
                    precio_total = detalle.cantidad * medicamento.precioCaja

                    # Crear detalle de factura
                    new_detalle = ModelFacturaDetalle(
                        factura_id=new_factura.idfactura,
                        medicamento_id=detalle.medicamento_id,
                        cantidad=detalle.cantidad,
                        precio_unitario=medicamento.precioCaja,
                        precio_total=precio_total,
                        tipo_venta='caja'  # Asegúrate de asignar correctamente este campo
                    )
                else:
                    raise HTTPException(status_code=400, detail=f"Tipo de venta desconocido para el detalle con medicamento ID: {detalle.medicamento_id}")
                
                self.db.add(new_detalle)
        
        self.db.commit()
        self.db.refresh(new_factura)

        return new_factura

        


