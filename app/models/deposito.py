from app.connection_database import get_db_connection
from datetime import datetime

class deposito:
    def __init__(self, id=None, cuenta_id=None, monto=None, fecha=None, estado='en proceso'):
        self.id = id
        self.cuenta_id = cuenta_id
        self.monto = monto
        self.fecha = fecha
        self.estado = estado

    @staticmethod
    def crear_deposito(id_cuenta, monto):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Iniciar transacción
            cursor.execute("START TRANSACTION")
            
            # Verificar que la cuenta existe
            cursor.execute("""
                SELECT id_cuenta FROM cuentas 
                WHERE id_cuenta = %s 
                FOR UPDATE
            """, (id_cuenta,))
            
            cuenta = cursor.fetchone()
            if not cuenta:
                raise ValueError("Cuenta no encontrada")
            
            # Crear el depósito con los nombres correctos de las columnas
            cursor.execute("""
                INSERT INTO deposito (id_cuenta, monto, fecha_deposito, canal, estado) 
                VALUES (%s, %s, NOW(), 'web', 'completado')
            """, (id_cuenta, monto))
            
            # Actualizar el saldo
            cursor.execute("""
                UPDATE cuentas 
                SET saldo_actual = saldo_actual + %s 
                WHERE id_cuenta = %s
            """, (monto, id_cuenta))
            
            conn.commit()
            return cursor.lastrowid
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close() 