from app.extensions import ma
from app.models.transaccion import Transaccion
from marshmallow import fields

class TransaccionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaccion
        
    id_transaccion = ma.auto_field()
    id_cuenta_origen = ma.auto_field()
    id_cuenta_envio = ma.auto_field()
    monto = fields.Decimal(as_string=True)
    fecha_transaccion = fields.DateTime('%Y-%m-%d %H:%M:%S')
    canal = ma.auto_field()
    estado = ma.auto_field()
    descripcion = ma.auto_field()