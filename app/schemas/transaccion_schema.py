from app.extensions import ma
from app.models.transaccion import Transaccion
from marshmallow import fields

class TransaccionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaccion
        
    id_transaccion = fields.Int()
    id_cuenta_origen = fields.Int()
    id_cuenta_envio = fields.Int()
    monto = fields.Decimal(as_string=True)
    fecha_transaccion = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    canal = fields.String()
    estado = fields.String()