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
            # Verificar si el servicio existe
            cursor.execute("SELECT id_servicio FROM servicios WHERE id_servicio = %s", (servicio_id,))
            servicio = cursor.fetchone()
            
            if servicio is None:
                raise ValueError("El servicio no existe")
            
            # Verificar saldo suficiente
            cursor.execute("SELECT saldo_actual FROM cuentas WHERE id_cuenta = %s", (cuenta_id,))
            saldo_actual = cursor.fetchone()
            
            if saldo_actual is None:
                raise ValueError("Cuenta no encontrada")
            
            if float(saldo_actual[0]) < float(monto):
                raise ValueError("Saldo insuficiente")
            
            # Iniciar transacción
            cursor.execute("START TRANSACTION")
            
            # Crear el pago
            sql_pago = """INSERT INTO pagosservicios 
                         (id_cuenta, id_servicio, monto, fecha_pago, estado) 
                         VALUES (%s, %s, %s, NOW(), 'completado')"""
            cursor.execute(sql_pago, (cuenta_id, servicio_id, monto))
            
            # Actualizar el saldo
            sql_actualizar = """UPDATE cuentas SET saldo_actual = saldo_actual - %s 
                              WHERE id_cuenta = %s"""
            cursor.execute(sql_actualizar, (monto, cuenta_id))
            
            conn.commit()
            return cursor.lastrowid
            
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
            FROM Pagos_servicios ps
            JOIN servicios s ON ps.servicio_id = s.id
            JOIN cuentas c ON ps.cuenta_id = c.id
            WHERE c.cliente_id = %s
            ORDER BY ps.fecha DESC
        """
        
        cursor.execute(sql, (cliente_id,))
        pagos = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return pagos 