from app.extensions import ma
from app.models.retiro import Retiro
from marshmallow import fields

class RetiroSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Retiro
        
    id_retiro = ma.auto_field()
    id_cuenta = ma.auto_field()
    monto = fields.Decimal(as_string=True)
    fecha_retiro = fields.DateTime('%Y-%m-%d %H:%M:%S')
    canal_retiro = ma.auto_field()
    codigo_retiro = ma.auto_field()
    estado = ma.auto_field()