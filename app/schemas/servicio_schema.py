from app.extensions import ma
from app.models.servicio import Servicio
from marshmallow import fields
class ServicioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Servicio
        
    id_servicio = fields.Int()
    nombre_servicio = fields.String()
    empresa = fields.String()
    tipo_servicio = fields.String()
    estado = fields.String()