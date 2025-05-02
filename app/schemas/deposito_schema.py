from app.extensions import ma
from app.models.deposito import Deposito
from marshmallow import fields

class DepositoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Deposito
        
    id_deposito = ma.auto_field()
    id_cuenta = ma.auto_field()
    monto = fields.Decimal(as_string=True)
    fecha_deposito = fields.DateTime('%Y-%m-%d %H:%M:%S')
    canal = ma.auto_field()
    estado = ma.auto_field()