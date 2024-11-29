from app.connection_database import get_db_connection
from datetime import datetime
from app.utils.encryption import decrypt_data

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
    def transferir_dinero(cuenta_origen_id, numero_telefono_destino, monto, descripcion):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Verificar que la cuenta origen existe
            cursor.execute("SELECT * FROM Cuentas WHERE id_cuenta = %s", (cuenta_origen_id,))
            cuenta_origen = cursor.fetchone()
            if not cuenta_origen:
                raise ValueError("Cuenta origen no encontrada")
            
            # Obtener todas las cuentas y buscar coincidencia desencriptando
            cursor.execute("SELECT * FROM Cuentas")
            cuentas = cursor.fetchall()
            cuenta_destino = None
            
            print(f"Buscando cuenta con número: {numero_telefono_destino}")  # Debug
            
            for cuenta in cuentas:
                try:
                    telefono_encriptado = cuenta['numero_telefono_ingreso']
                    if telefono_encriptado:
                        print(f"Cuenta ID {cuenta['id_cuenta']} - Intentando desencriptar")
                        try:
                            telefono_desencriptado = decrypt_data(telefono_encriptado)
                            print(f"Teléfono desencriptado: {telefono_desencriptado}")
                            
                            if telefono_desencriptado == numero_telefono_destino:
                                cuenta_destino = cuenta
                                break
                        except Exception as decrypt_error:
                            print(f"Error específico de desencriptación: {str(decrypt_error)}")
                            continue
                except Exception as e:
                    print(f"Error general al procesar cuenta {cuenta['id_cuenta']}: {str(e)}")
                    continue
            
            if not cuenta_destino:
                raise ValueError("Cuenta destino no encontrada")
            
            # Verificar que no es la misma cuenta
            if cuenta_origen_id == cuenta_destino['id_cuenta']:
                raise ValueError("No puedes transferir dinero a tu propia cuenta")
            
            # Verificar saldo suficiente
            if cuenta_origen['saldo_actual'] < monto:
                raise ValueError("Saldo insuficiente")
            
            # Realizar la transferencia
            cursor.execute("UPDATE Cuentas SET saldo_actual = saldo_actual - %s WHERE id_cuenta = %s", 
                         (monto, cuenta_origen_id))
            cursor.execute("UPDATE Cuentas SET saldo_actual = saldo_actual + %s WHERE id_cuenta = %s", 
                         (monto, cuenta_destino['id_cuenta']))
            
            # Registrar la transacción
            sql = """INSERT INTO Transaccion (id_cuenta_origen, id_cuenta_envio, monto, 
                    fecha_transaccion, canal, estado) VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (cuenta_origen_id, cuenta_destino['id_cuenta'], monto, 
                      datetime.now(), 'web', 'completado')
            
            cursor.execute(sql, valores)
            conn.commit()
            
            # Retornar nuevo saldo
            cursor.execute("SELECT saldo_actual FROM Cuentas WHERE id_cuenta = %s", (cuenta_origen_id,))
            nuevo_saldo = cursor.fetchone()['saldo_actual']
            return nuevo_saldo
            
        except Exception as e:
            print(f"Error en transferencia: {str(e)}")  # Debug
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear_transaccion(cuenta_origen, cuenta_destino, monto, tipo, descripcion=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """INSERT INTO Transaccion (id_cuenta_origen, id_cuenta_envio, monto, 
                fecha_transaccion, canal, estado) VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (cuenta_origen, cuenta_destino, monto, tipo, 
                  datetime.now(), 'completada', descripcion)
        
        cursor.execute(sql, valores)
        conn.commit()
        
        transaccion_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return transaccion_id 
    
    def obtener_transacciones_usuario(usuario_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transaccion WHERE id_cuenta_origen = %s", (usuario_id,))
        transacciones = cursor.fetchall()
        return transacciones
