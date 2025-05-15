from app.extensions import ma
from app.models.cliente import Cliente
from marshmallow import fields

class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente
        
    id_cliente = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    documento_identidad = fields.Str(required=True)
    correo_electronico = fields.Email(required=True)
    fecha_nacimiento = fields.Date(format='%Y-%m-%d')
    fecha_registro = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
   
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"