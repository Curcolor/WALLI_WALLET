from app.extensions import db
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from app.utils.encryption import encrypt_data, decrypt_data

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    _documento_identidad = db.Column('documento_identidad', db.String(255), nullable=False)
    _correo_electronico = db.Column('correo_electronico', db.String(255), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación
    cuenta = db.relationship('Cuenta', uselist=False, back_populates='cliente')
    
    # Propiedades híbridas para encriptar/desencriptar documento de identidad
    @hybrid_property
    def documento_identidad(self):
        return decrypt_data(self._documento_identidad)
    
    @documento_identidad.setter
    def documento_identidad(self, value):
        self._documento_identidad = encrypt_data(value)
    
    # Propiedades híbridas para encriptar/desencriptar correo electrónico
    @hybrid_property
    def correo_electronico(self):
        return decrypt_data(self._correo_electronico)
    
    @correo_electronico.setter
    def correo_electronico(self, value):
        self._correo_electronico = encrypt_data(value)
    
    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellido}>'