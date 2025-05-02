from app.extensions import ma
from app.models.cliente import Cliente
from marshmallow import fields

class ClienteSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Cliente
        
    id_cliente = ma.auto_field()
    nombre = ma.auto_field()
    apellido = ma.auto_field()
    documento_identidad = ma.auto_field()
    correo_electronico = ma.auto_field()
    fecha_nacimiento = fields.Date('%Y-%m-%d')
    fecha_registro = fields.DateTime('%Y-%m-%d %H:%M:%S')
    nombre_completo = fields.Method('get_nombre_completo')
    
    def get_nombre_completo(self, obj):
        return f"{obj.nombre} {obj.apellido}"