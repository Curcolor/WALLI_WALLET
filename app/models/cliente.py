from app.connection_database import get_db_connection

class Cliente:
    @staticmethod
    def crear_cliente_con_cuenta(**datos):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            conn.start_transaction()
            
            cursor.execute("""
                INSERT INTO Clientes (nombre, apellido, documento_identidad, 
                                    correo_electronico, fecha_nacimiento)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                datos['nombre'],
                datos['apellido'],
                datos['documento_identidad'],
                datos['correo_electronico'],
                datos['fecha_nacimiento']
            ))
            
            cliente_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO Cuentas (id_cliente, tipo_cuenta, clave_ingreso, 
                                   numero_telefono_ingreso)
                VALUES (%s, %s, %s, %s)
            """, (
                cliente_id,
                datos['tipo_cuenta'],
                datos['clave_ingreso'],  # Clave en texto plano
                datos['numero_telefono_ingreso']
            ))
            
            conn.commit()
            return cliente_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()