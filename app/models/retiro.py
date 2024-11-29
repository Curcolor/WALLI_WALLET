from app.connection_database import get_db_connection
from datetime import datetime
import random
import string

class Retiro:
    def __init__(self, id=None, cuenta_id=None, monto=None, fecha=None, estado='en proceso'):
        self.id = id
        self.cuenta_id = cuenta_id
        self.monto = monto
        self.fecha = fecha
        self.estado = estado

    @staticmethod
    def generar_codigo_retiro(longitud=6):
        """Genera un código aleatorio para el retiro"""
        caracteres = string.digits  # Solo números
        return ''.join(random.choice(caracteres) for _ in range(longitud))

    @staticmethod
    def crear_retiro(cuenta_id, monto):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar saldo suficiente
            cursor.execute("SELECT saldo_actual FROM Cuentas WHERE id_cuenta = %s", (cuenta_id,))
            saldo_actual = cursor.fetchone()[0]
            
            if saldo_actual < monto:
                raise ValueError("Saldo insuficiente")
            
            # Iniciar transacción
            cursor.execute("START TRANSACTION")
            
            # Generar código de retiro
            codigo_retiro = Retiro.generar_codigo_retiro()
            
            # Crear el retiro
            sql_retiro = """INSERT INTO Retiros 
                          (id_cuenta, monto, fecha_retiro, canal_retiro, codigo_retiro, estado) 
                          VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_retiro, (
                cuenta_id, 
                monto, 
                datetime.now(),
                'web',
                codigo_retiro,
                'completado'
            ))
            
            # Actualizar el saldo
            sql_actualizar = """UPDATE Cuentas 
                              SET saldo_actual = saldo_actual - %s 
                              WHERE id_cuenta = %s"""
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