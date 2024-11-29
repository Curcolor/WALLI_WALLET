from app.connection_database import get_db_connection
from datetime import datetime

class Transaccion:
    def __init__(self, id=None, cuenta_origen=None, cuenta_destino=None, 
                 monto=None, tipo=None, fecha=None, estado='pendiente'):
        self.id = id
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino
        self.monto = monto
        self.tipo = tipo
        self.fecha = fecha
        self.estado = estado

    @staticmethod
    def obtener_transacciones_usuario(id_cuenta):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT 
                    id_cuenta_envio,
                    monto,
                    fecha_transaccion,
                    canal,
                    estado
                FROM transaccion
                WHERE id_cuenta_origen = %s
                ORDER BY fecha_transaccion DESC
                LIMIT 10
            """
            
            cursor.execute(query, (id_cuenta,))
            transacciones = cursor.fetchall()
            
            return transacciones
            
        except Exception as e:
            print(f"Error al obtener transacciones: {str(e)}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear_transaccion(cuenta_origen, cuenta_destino, monto, tipo):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """INSERT INTO Transacciones (cuenta_origen, cuenta_destino, monto, 
                tipo, fecha, estado) VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (cuenta_origen, cuenta_destino, monto, tipo, 
                  datetime.now(), 'completada')
        
        cursor.execute(sql, valores)
        conn.commit()
        
        transaccion_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return transaccion_id 