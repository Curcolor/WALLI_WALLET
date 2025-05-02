from app.extensions import ma
from marshmallow import fields, Schema

class TransaccionResumenSchema(Schema):
    tipo_transaccion = fields.String(required=True)
    monto = fields.Decimal(as_string=True, required=True)
    fecha_transaccion = fields.DateTime('%Y-%m-%d %H:%M:%S', required=True)
    descripcion = fields.String()
    estado = fields.String(required=True)