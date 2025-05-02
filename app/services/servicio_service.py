from app.models import Servicio, PagoServicio
from app.extensions import db

class ServicioService:
    @staticmethod
    def get_all_servicios():
        """Obtiene todos los servicios activos"""
        return Servicio.query.filter_by(estado='activo').all()
    
    @staticmethod
    def get_servicio(servicio_id):
        """Obtiene un servicio por su ID"""
        return Servicio.query.get(servicio_id)
    
    @staticmethod
    def crear_servicio(nombre_servicio, empresa, tipo_servicio):
        """Crea un nuevo servicio"""
        servicio = Servicio(
            nombre_servicio=nombre_servicio,
            empresa=empresa,
            tipo_servicio=tipo_servicio,
            estado='activo'
        )
        
        db.session.add(servicio)
        db.session.commit()
        
        return servicio
    
    @staticmethod
    def obtener_servicios():
        """
        Método compatible con la versión original que devuelve 
        los servicios en formato de diccionario
        """
        servicios = Servicio.query.filter_by(estado='activo').all()
        resultado = []
        
        for servicio in servicios:
            resultado.append({
                'id_servicio': servicio.id_servicio,
                'nombre_servicio': servicio.nombre_servicio,
                'empresa': servicio.empresa,
                'tipo_servicio': servicio.tipo_servicio
            })
            
        return resultado