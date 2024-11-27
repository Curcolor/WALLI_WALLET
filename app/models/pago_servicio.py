from app.connection_database import get_db_connection
from datetime import datetime

class PagoServicio:
    def __init__(self, id=None, cuenta_id=None, servicio_id=None, 
                 monto=None, fecha=None, estado='en proceso'):
        self.id = id
        self.cuenta_id = cuenta_id
        self.servicio_id = servicio_id
        self.monto = monto
        self.fecha = fecha
        self.estado = estado

    @staticmethod
    def crear_pago(cuenta_id, servicio_id, monto):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar saldo suficiente
            cursor.execute("SELECT saldo FROM Cuentas WHERE id = %s", (cuenta_id,))
            saldo_actual = cursor.fetchone()[0]
            
            if saldo_actual < monto:
                raise ValueError("Saldo insuficiente")
            
            # Iniciar transacción
            cursor.execute("START TRANSACTION")
            
            # Crear el pago
            sql_pago = """INSERT INTO Pagos_Servicios 
                         (cuenta_id, servicio_id, monto, fecha, estado) 
                         VALUES (%s, %s, %s, %s, 'completado')"""
            cursor.execute(sql_pago, (cuenta_id, servicio_id, monto, datetime.now()))
            
            # Actualizar el saldo
            sql_actualizar = """UPDATE Cuentas SET saldo = saldo - %s 
                              WHERE id = %s"""
            cursor.execute(sql_actualizar, (monto, cuenta_id))
            
            conn.commit()
            pago_id = cursor.lastrowid
            
            return pago_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close() 

    @staticmethod
    def obtener_pagos_por_cliente(cliente_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT ps.*, s.nombre as servicio_nombre 
            FROM Pagos_Servicios ps
            JOIN Servicios s ON ps.servicio_id = s.id
            JOIN Cuentas c ON ps.cuenta_id = c.id
            WHERE c.cliente_id = %s
            ORDER BY ps.fecha DESC
        """
        
        cursor.execute(sql, (cliente_id,))
        pagos = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return pagos 