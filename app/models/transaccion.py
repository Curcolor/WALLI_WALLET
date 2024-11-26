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