from flask_login import UserMixin
from app.connection_database import get_db_connection

class Cuenta(UserMixin):
    def __init__(self, id=None, id_cliente=None, saldo_actual=0.00, tipo_cuenta='ahorro', 
                 clave_ingreso=None, numero_telefono_ingreso=None, estado='activa'):
        self.id = id
        self.id_cliente = id_cliente
        self.saldo_actual = saldo_actual
        self.tipo_cuenta = tipo_cuenta
        self.clave_ingreso = clave_ingreso
        self.numero_telefono_ingreso = numero_telefono_ingreso
        self.estado = estado

    def get_id(self):
        return str(self.id)

    @staticmethod
    def verificar_login(numero_telefono, clave):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            print(f"Verificando login para teléfono: {numero_telefono}")
            
            cursor.execute("""
                SELECT id_cuenta, clave_ingreso, numero_telefono_ingreso 
                FROM Cuentas 
                WHERE numero_telefono_ingreso = %s 
                AND clave_ingreso = %s
            """, (numero_telefono, clave))
            
            cuenta = cursor.fetchone()
            print(f"Cuenta encontrada: {cuenta}")  # Debug
            
            return cuenta
            
        except Exception as e:
            print(f"Error en verificar_login: {str(e)}")
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear_cuenta(id_cliente, tipo_cuenta, clave_ingreso, numero_telefono_ingreso):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Cuentas (id_cliente, tipo_cuenta, clave_ingreso, 
                                   numero_telefono_ingreso, saldo_actual)
                VALUES (%s, %s, %s, %s, 0)
            """, (id_cliente, tipo_cuenta, clave_ingreso, numero_telefono_ingreso))
            
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
            
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT * FROM Cuentas WHERE id_cuenta = %s
            """, (user_id,))
            
            cuenta_data = cursor.fetchone()
            print(f"Datos de cuenta obtenidos: {cuenta_data}")  # Debug
            
            if cuenta_data:
                return Cuenta(
                    id=cuenta_data['id_cuenta'],
                    id_cliente=cuenta_data['id_cliente'],
                    saldo_actual=cuenta_data['saldo_actual'],
                    tipo_cuenta=cuenta_data['tipo_cuenta'],
                    numero_telefono_ingreso=cuenta_data['numero_telefono_ingreso']
                )
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_saldo(cuenta_id):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT saldo_actual 
                FROM Cuentas 
                WHERE id_cuenta = %s
            """, (cuenta_id,))
            
            resultado = cursor.fetchone()
            print(f"Saldo obtenido: {resultado}")  # Debug
            return float(resultado['saldo_actual']) if resultado else 0
            
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def retirar_dinero(cuenta_id, monto):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Iniciar transacción
            conn.start_transaction()
            
            # Verificar saldo disponible
            cursor.execute("""
                SELECT saldo_actual, estado 
                FROM Cuentas 
                WHERE id_cuenta = %s 
                FOR UPDATE
            """, (cuenta_id,))
            
            cuenta_data = cursor.fetchone()
            print(f"Datos de cuenta: {cuenta_data}")  # Debug
            
            if not cuenta_data:
                raise ValueError("Cuenta no encontrada")
            
            saldo_actual = float(cuenta_data['saldo_actual'])
            monto_retiro = float(monto)
            
            if saldo_actual < monto_retiro:
                raise ValueError("Saldo insuficiente")
            
            nuevo_saldo = saldo_actual - monto_retiro
            print(f"Calculando nuevo saldo: {saldo_actual} - {monto_retiro} = {nuevo_saldo}")  # Debug
            
            # Realizar el retiro
            cursor.execute("""
                UPDATE Cuentas 
                SET saldo_actual = %s 
                WHERE id_cuenta = %s
            """, (nuevo_saldo, cuenta_id))
            
            # Verificar que la actualización fue exitosa
            if cursor.rowcount == 0:
                raise Exception("No se pudo actualizar el saldo")
            
            conn.commit()
            return nuevo_saldo
            
        except Exception as e:
            conn.rollback()
            print(f"Error en retirar_dinero: {str(e)}")  # Debug
            raise e
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def transferir_dinero(cuenta_origen_id, numero_telefono_destino, monto, descripcion=None):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Iniciar transacción
            conn.start_transaction()
            
            # Verificar cuenta origen y su saldo
            cursor.execute("""
                SELECT c.saldo_actual, c.estado, c.numero_telefono_ingreso 
                FROM Cuentas c
                WHERE c.id_cuenta = %s 
                FOR UPDATE
            """, (cuenta_origen_id,))
            
            cuenta_origen = cursor.fetchone()
            if not cuenta_origen:
                raise ValueError("Cuenta origen no encontrada")
            if cuenta_origen['estado'] != 'activa':
                raise ValueError("Cuenta origen no está activa")
            
            # Evitar transferencia al mismo número
            if cuenta_origen['numero_telefono_ingreso'] == numero_telefono_destino:
                raise ValueError("No puedes transferir dinero a tu propia cuenta")
            
            # Verificar cuenta destino usando el número de teléfono
            cursor.execute("""
                SELECT id_cuenta, estado 
                FROM Cuentas 
                WHERE numero_telefono_ingreso = %s 
                FOR UPDATE
            """, (numero_telefono_destino,))
            
            cuenta_destino = cursor.fetchone()
            if not cuenta_destino:
                raise ValueError("No se encontró una cuenta asociada a ese número de teléfono")
            if cuenta_destino['estado'] != 'activa':
                raise ValueError("La cuenta destino no está activa")
            
            cuenta_destino_id = cuenta_destino['id_cuenta']
            
            # Verificar saldo suficiente
            saldo_actual = float(cuenta_origen['saldo_actual'])
            monto_transferencia = float(monto)
            
            if saldo_actual < monto_transferencia:
                raise ValueError("Saldo insuficiente para realizar la transferencia")
            
            # Realizar la transferencia
            # Restar de la cuenta origen
            cursor.execute("""
                UPDATE Cuentas 
                SET saldo_actual = saldo_actual - %s 
                WHERE id_cuenta = %s
            """, (monto_transferencia, cuenta_origen_id))
            
            # Sumar a la cuenta destino
            cursor.execute("""
                UPDATE Cuentas 
                SET saldo_actual = saldo_actual + %s 
                WHERE id_cuenta = %s
            """, (monto_transferencia, cuenta_destino_id))
            
            # Registrar la transacción usando los nombres correctos de las columnas
            cursor.execute("""
                INSERT INTO transaccion 
                (id_cuenta_origen, id_cuenta_envio, monto, fecha_transaccion, canal, estado) 
                VALUES (%s, %s, %s, NOW(), 'web', 'completado')
            """, (cuenta_origen_id, cuenta_destino_id, monto_transferencia))
            
            conn.commit()
            
            # Obtener nuevo saldo de la cuenta origen
            cursor.execute("""
                SELECT saldo_actual 
                FROM Cuentas 
                WHERE id_cuenta = %s
            """, (cuenta_origen_id,))
            
            nuevo_saldo = cursor.fetchone()['saldo_actual']
            return float(nuevo_saldo)
            
        except Exception as e:
            conn.rollback()
            print(f"Error en transferir_dinero: {str(e)}")  # Debug
            raise e
        finally:
            cursor.close()
            conn.close()