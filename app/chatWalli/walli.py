import ollama
from app.models.transaccion import Transaccion

class Walli:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id

    def obtener_resumen_estado_cuenta(self):
        # Conectar a la base de datos
        transacciones = Transaccion.obtener_transacciones_usuario(self.usuario_id)
        # Generar un resumen de las transacciones
        resumen = f"Resumen de transacciones para el usuario {self.usuario_id}:\n"
        for transaccion in transacciones:
            id_transaccion, cuenta_origen, cuenta_destino, monto, tipo, fecha, canal, estado = transaccion
            resumen += f"{fecha}: {tipo} de ${monto} enviado a {cuenta_destino} por {canal} desde {cuenta_origen} con estado {estado} con id {id_transaccion}\n"
        
        return resumen
    
    def obtener_respuesta_con_resumen(self, pregunta):
        resumen_estado = self.obtener_resumen_estado_cuenta()
        prompt = f"""
        Usuario: {pregunta}
        Información del estado de cuenta: {resumen_estado} 
        Responde al usuario sobre su estado de cuenta usando la información proporcionada.
        """
    
        response = ollama.generate(
            model="llama3.1",
            prompt=prompt
        )
        return response['response']
