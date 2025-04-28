from app.connection_database import get_db_connection
from app.utils.encryption import encrypt_data, decrypt_data

class Cliente:
    @staticmethod
    def crear_cliente_con_cuenta(**datos):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            
            # Encriptar datos sensibles
            documento_encriptado = encrypt_data(datos['documento_identidad'])
            correo_encriptado = encrypt_data(datos['correo_electronico'])
            
            cursor.execute("""
                INSERT INTO clientes (nombre, apellido, documento_identidad, 
                                    correo_electronico, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                datos['nombre'],
                datos['apellido'],
                documento_encriptado,
                correo_encriptado,
                datos['fecha_nacimiento']
            ))
            
            cliente_id = cursor.lastrowid
            
            # Encriptar datos de cuenta
            clave_encriptada = encrypt_data(datos['clave_ingreso'])
            telefono_encriptado = encrypt_data(datos['numero_telefono_ingreso'])
            
            cursor.execute("""
                INSERT INTO cuentas (id_cliente, tipo_cuenta, clave_ingreso, 
                                   numero_telefono_ingreso)
                VALUES (%s, %s, %s, %s)
            """, (
                cliente_id,
                datos['tipo_cuenta'],
                clave_encriptada,
                telefono_encriptado
            ))
            
            conn.commit()
            return cliente_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()