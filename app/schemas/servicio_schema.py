from app.extensions import ma
from app.models.servicio import Servicio

class ServicioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Servicio
        
    id_servicio = ma.auto_field()
    nombre_servicio = ma.auto_field()
    empresa = ma.auto_field()
    tipo_servicio = ma.auto_field()
    estado = ma.auto_field()