from app.extensions import db
from datetime import datetime

class Deposito(db.Model):
    __tablename__ = 'deposito'
    
    id_deposito = db.Column(db.Integer, primary_key=True)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id_cuenta'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_deposito = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canal = db.Column(db.String(50), default='web', nullable=False)
    estado = db.Column(db.String(20), default='completado', nullable=False)
    
    # Relación
    cuenta = db.relationship('Cuenta', back_populates='depositos')
    
    def __repr__(self):
        return f'<Depósito {self.id_deposito} - ${self.monto}>'