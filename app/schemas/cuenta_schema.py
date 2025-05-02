from app.extensions import ma
from app.models.cuenta import Cuenta
from marshmallow import fields

class CuentaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cuenta
        
    id_cuenta = ma.auto_field()
    id_cliente = ma.auto_field()
    saldo_actual = fields.Decimal(as_string=True)
    tipo_cuenta = ma.auto_field()
    fecha_apertura = fields.DateTime('%Y-%m-%d %H:%M:%S')
    numero_telefono_ingreso = ma.auto_field()
    estado = ma.auto_field()