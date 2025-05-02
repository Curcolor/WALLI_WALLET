from app.extensions import ma
from app.models.pago_servicio import PagoServicio
from marshmallow import fields

class PagoServicioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PagoServicio
        
    id_pago = fields.Int()
    id_cuenta = fields.Int()
    id_servicio = fields.Int()
    monto = fields.Decimal(as_string=True)
    fecha_pago = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    referencia = fields.String()
    estado = fields.String()