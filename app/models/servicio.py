from app.extensions import db

class Servicio(db.Model):
    __tablename__ = 'servicios'
    
    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(255), nullable=False)
    empresa = db.Column(db.String(255), nullable=True)
    tipo_servicio = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(20), default='activo', nullable=False)
    
    # Relación
    pagos = db.relationship('PagoServicio', back_populates='servicio')
    
    def __repr__(self):
        return f'<Servicio {self.nombre_servicio}>'