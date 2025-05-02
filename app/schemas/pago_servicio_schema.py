from app.extensions import ma
from app.models.pago_servicio import PagoServicio
from marshmallow import fields

class PagoServicioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PagoServicio
        
    id_pago = ma.auto_field()
    id_cuenta = ma.auto_field()
    id_servicio = ma.auto_field()
    monto = fields.Decimal(as_string=True)
    fecha_pago = fields.DateTime('%Y-%m-%d %H:%M:%S')
    referencia = ma.auto_field()
    estado = ma.auto_field()