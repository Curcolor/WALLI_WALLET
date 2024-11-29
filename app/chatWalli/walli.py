import ollama
from app.models.transaccion import Transaccion
from app.connection_database import get_db_connection as get_db

class Walli:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id

    def obtener_info_cuenta(self):
        try:
            db = get_db()
            cursor = db.cursor()
            
            query = """
                SELECT 
                    c.nombre,
                    c.apellido,
                    cu.tipo_cuenta,
                    cu.saldo_actual,
                    cu.fecha_apertura,
                    cu.estado
                FROM clientes c
                INNER JOIN cuentas cu ON c.id_cliente = cu.id_cliente
                WHERE cu.id_cuenta = %s
            """
            
            cursor.execute(query, (self.usuario_id,))
            resultado = cursor.fetchone()
            
            if resultado:
                nombre, apellido, tipo_cuenta, saldo, fecha_apertura, estado = resultado
                info_cuenta = {
                    "nombre_completo": f"{nombre} {apellido}",
                    "tipo_cuenta": tipo_cuenta,
                    "saldo_actual": float(saldo),
                    "fecha_apertura": fecha_apertura.strftime("%Y-%m-%d"),
                    "estado_cuenta": estado
                }
                return info_cuenta
            else:
                return None
                
        except Exception as e:
            print(f"Error al obtener información de la cuenta: {str(e)}")
            return None
        finally:
            cursor.close()

    def obtener_resumen_estado_cuenta(self):
        info_cuenta = self.obtener_info_cuenta()
        if not info_cuenta:
            return "No se pudo obtener la información de la cuenta"
        
        # Conectar a la base de datos
        transacciones = Transaccion.obtener_transacciones_usuario(self.usuario_id)
        
        # Generar un resumen de las transacciones
        resumen = f"""
        Información de la cuenta:
        Cliente: {info_cuenta['nombre_completo']}
        Tipo de cuenta: {info_cuenta['tipo_cuenta']}
        Saldo actual: ${info_cuenta['saldo_actual']}
        Fecha de apertura: {info_cuenta['fecha_apertura']}
        Estado de la cuenta: {info_cuenta['estado_cuenta']}

        Historial de transacciones:
        """
        
        for transaccion in transacciones:
            id_transaccion, cuenta_origen, cuenta_destino, monto, tipo, fecha, canal, estado = transaccion
            resumen += f"{fecha}: {tipo} de ${monto} enviado a {cuenta_destino} por {canal} desde {cuenta_origen} con estado {estado} con id {id_transaccion}\n"
        
        return resumen
    
    def obtener_respuesta_con_resumen(self, pregunta):
        info_cuenta = self.obtener_info_cuenta()
        if not info_cuenta:
            return "Lo siento, no pude obtener la información de tu cuenta."
            
        resumen_estado = self.obtener_resumen_estado_cuenta()
        
        prompt = f"""
        Contexto: Eres un asistente de una Billetera Digital llamada WALLI que ayuda a los clientes con información sobre sus cuentas.
        
        Información del cliente:
        - Nombre: {info_cuenta['nombre_completo']}
        - Tipo de cuenta: {info_cuenta['tipo_cuenta']}
        - Saldo actual: ${info_cuenta['saldo_actual']}
        - Estado de la cuenta: {info_cuenta['estado_cuenta']}
        
        Pregunta del cliente: {pregunta}
        
        Información detallada de la cuenta y transacciones:
        {resumen_estado}
        
        Instrucciones:
        1. Responde al cliente llamándolo por su nombre
        2. Sé amable y profesional
        3. Usa la información proporcionada para dar respuestas precisas
        4. Si te preguntan por el saldo o transacciones, usa los datos exactos proporcionados
        5. Si la pregunta no está relacionada con la información disponible, indícalo amablemente
        """
    
        response = ollama.generate(
            model="llama3.1",
            prompt=prompt
        )
        return response['response']
