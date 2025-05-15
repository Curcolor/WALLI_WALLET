from app.extensions import db
from datetime import datetime

class Retiro(db.Model):
    __tablename__ = 'retiros'
    
    id_retiro = db.Column(db.Integer, primary_key=True)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id_cuenta'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_retiro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    canal_retiro = db.Column(db.String(50), default='web', nullable=False)
    codigo_retiro = db.Column(db.String(10), nullable=True)
    estado = db.Column(db.String(20), default='completado', nullable=False)
    
    # Relación
    cuenta = db.relationship('Cuenta', back_populates='retiros')
    
    def __repr__(self):
        return f'<Retiro {self.id_retiro} - ${self.monto}>'