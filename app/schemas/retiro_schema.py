from app.extensions import ma
from app.models.retiro import Retiro
from marshmallow import fields

class RetiroSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Retiro
        
    id_retiro = fields.Int()
    id_cuenta = fields.Int()
    monto = fields.Decimal(as_string=True)
    fecha_retiro = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    canal_retiro = fields.String()
    codigo_retiro = fields.String()
    estado = fields.String()