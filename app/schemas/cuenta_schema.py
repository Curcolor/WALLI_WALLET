from app.extensions import ma
from app.models.cuenta import Cuenta
from marshmallow import fields

class CuentaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cuenta
        
    id_cuenta = fields.Int()
    id_cliente = fields.Int()
    saldo_actual = fields.Decimal(as_string=True)
    tipo_cuenta = fields.String()
    fecha_apertura = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    numero_telefono_ingreso = fields.String()
    estado = fields.String()