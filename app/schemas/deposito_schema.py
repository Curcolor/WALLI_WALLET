from app.extensions import ma
from app.models.deposito import Deposito
from marshmallow import fields

class DepositoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Deposito
        
    id_deposito = fields.Int()
    id_cuenta = fields.Int()
    monto = fields.Decimal(as_string=True)
    fecha_deposito = fields.DateTime('%Y-%m-%d %H:%M:%S')
    canal = fields.String()
    estado = fields.String()