from app.connection_database import get_db_connection

class Servicio:
    def __init__(self, id=None, nombre=None, descripcion=None, estado='ACTIVO'):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

    @staticmethod
    def crear_servicio(nombre, descripcion):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """INSERT INTO servicios (nombre, descripcion, estado) 
                VALUES (%s, %s, 'ACTIVO')"""
        cursor.execute(sql, (nombre, descripcion))
        
        conn.commit()
        servicio_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        return servicio_id

    @staticmethod
    def obtener_servicios():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM servicios")
        servicios = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return servicios