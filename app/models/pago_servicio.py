from app.extensions import db
from datetime import datetime
from app.models.cuenta import Cuenta
from app.models.servicio import Servicio

class PagoServicio(db.Model):
    __tablename__ = 'pagosservicios'
    
    id_pago = db.Column(db.Integer, primary_key=True)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id_cuenta'), nullable=False)
    id_servicio = db.Column(db.Integer, db.ForeignKey('servicios.id_servicio'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    referencia = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(20), default='completado', nullable=False)
    
    # Relaciones
    cuenta = db.relationship('Cuenta', back_populates='pagos_servicios')
    servicio = db.relationship('Servicio', back_populates='pagos')
    
    @classmethod
    def crear_pago(cls, cuenta_id, servicio_id, monto, referencia=None):
        """
        Método de clase para compatibilidad con código antiguo
        """
        # Verificar cuenta
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
        
        # Verificar servicio
        servicio = Servicio.query.get(servicio_id)
        if not servicio:
            raise ValueError("Servicio no encontrado")
            
        # Verificar saldo
        if float(cuenta.saldo_actual) < float(monto):
            raise ValueError("Saldo insuficiente")
            
        # Crear pago
        pago = cls(
            id_cuenta=cuenta_id,
            id_servicio=servicio_id,
            monto=monto,
            referencia=referencia,
            estado='completado'
        )
        
        # Actualizar saldo
        cuenta.saldo_actual = float(cuenta.saldo_actual) - float(monto)
        
        db.session.add(pago)
        db.session.commit()
        
        return pago.id_pago
    
    def __repr__(self):
        return f'<Pago Servicio {self.id_pago} - ${self.monto}>'