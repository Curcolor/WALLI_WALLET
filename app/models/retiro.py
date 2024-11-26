from app.connection_database import get_db_connection
from datetime import datetime

class Retiro:
    def __init__(self, id=None, cuenta_id=None, monto=None, fecha=None, estado='en proceso'):
        self.id = id
        self.cuenta_id = cuenta_id
        self.monto = monto
        self.fecha = fecha
        self.estado = estado

    @staticmethod
    def crear_retiro(cuenta_id, monto):
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
            
            # Crear el retiro
            sql_retiro = """INSERT INTO Retiros (cuenta_id, monto, fecha, estado) 
                          VALUES (%s, %s, %s, 'completado')"""
            cursor.execute(sql_retiro, (cuenta_id, monto, datetime.now()))
            
            # Actualizar el saldo
            sql_actualizar = """UPDATE Cuentas SET saldo = saldo - %s 
                              WHERE id = %s"""
            cursor.execute(sql_actualizar, (monto, cuenta_id))
            
            conn.commit()
            retiro_id = cursor.lastrowid
            
            return retiro_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close() 