from app.connection_database import get_db_connection
from app.extensions import db
from datetime import datetime
from app.utils.encryption import decrypt_data

class Transaccion(db.Model):
    __tablename__ = 'transaccion'
    
    id_transaccion = db.Column(db.Integer, primary_key=True)
    id_cuenta_origen = db.Column(db.Integer, db.ForeignKey('cuentas.id_cuenta'), nullable=False)
    id_cuenta_envio = db.Column(db.Integer, db.ForeignKey('cuentas.id_cuenta'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_transaccion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canal = db.Column(db.String(50), default='web', nullable=False)
    estado = db.Column(db.String(20), default='completado', nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    
    # Relaciones
    cuenta_origen = db.relationship('Cuenta', foreign_keys=[id_cuenta_origen], back_populates='transferencias_enviadas')
    cuenta_destino = db.relationship('Cuenta', foreign_keys=[id_cuenta_envio], back_populates='transferencias_recibidas')
    
    def __repr__(self):
        return f'<Transferencia {self.id_transaccion} - ${self.monto}>'
