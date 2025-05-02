from app.extensions import db
from datetime import datetime
from app.utils.encryption import encrypt_data, decrypt_data

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    documento_identidad = db.Column(db.String(255), nullable=False)
    correo_electronico = db.Column(db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    cuenta = db.relationship('Cuenta', uselist=False, back_populates='cliente')
    
    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellido}>'