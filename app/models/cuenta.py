from app.extensions import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

class Cuenta(db.Model, UserMixin):
    __tablename__ = 'cuentas'
    
    id_cuenta = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), unique=True)
    saldo_actual = db.Column(db.Numeric(10, 2), default=0.0, nullable=False)
    tipo_cuenta = db.Column(db.String(50), nullable=False)
    fecha_apertura = db.Column(db.DateTime, default=datetime.utcnow)
    _clave_ingreso = db.Column('clave_ingreso', db.String(255), nullable=False)
    numero_telefono_ingreso = db.Column(db.String(10), nullable=False, unique=True)
    estado = db.Column(db.String(20), default='activa')
    
    # Relaciones
    cliente = db.relationship('Cliente', back_populates='cuenta')
    depositos = db.relationship('Deposito', back_populates='cuenta')
    retiros = db.relationship('Retiro', back_populates='cuenta')
    pagos_servicios = db.relationship('PagoServicio', back_populates='cuenta')
    transferencias_enviadas = db.relationship('Transaccion', 
                                            foreign_keys='Transaccion.id_cuenta_origen',
                                            back_populates='cuenta_origen')
    transferencias_recibidas = db.relationship('Transaccion', 
                                             foreign_keys='Transaccion.id_cuenta_envio',
                                             back_populates='cuenta_destino')
    
    def get_id(self):
        return str(self.id_cuenta)
    
    @hybrid_property
    def clave_ingreso(self):
        return self._clave_ingreso
    
    @clave_ingreso.setter
    def clave_ingreso(self, clave):
        self._clave_ingreso = generate_password_hash(clave)
    
    def check_password(self, clave):
        return check_password_hash(self._clave_ingreso, clave)
    
    def __repr__(self):
        return f'<Cuenta {self.id_cuenta}>'