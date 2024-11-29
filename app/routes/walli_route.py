from app.chatWalli.walli import Walli
from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
import logging
from werkzeug.exceptions import BadRequest

bp = Blueprint('walli', __name__, url_prefix='/api/walli')

chat_history = []

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@bp.route('/send', methods=['POST'])
@login_required  # Esto asegura que el usuario esté autenticado
def send_message():
    try:
        logger.debug("Iniciando procesamiento de mensaje...")
        
        # Verificar autenticación
        if not current_user.is_authenticated:
            logger.error("Usuario no autenticado")
            return jsonify({"error": "Debe iniciar sesión"}), 401

        # Obtener ID del usuario actual
        usuario_id = current_user.id
        logger.debug(f"Usuario autenticado con ID: {usuario_id}")

        # Obtener datos JSON
        try:
            data = request.get_json()
            if not data:
                logger.error("No se recibieron datos JSON")
                return jsonify({"error": "No se recibieron datos JSON"}), 400
            
            user_input = data.get('message')
            if not user_input:
                logger.error("Mensaje vacío")
                return jsonify({"error": "El mensaje no puede estar vacío"}), 400

            logger.debug(f"Mensaje recibido: {user_input}")

        except Exception as e:
            logger.error(f"Error al procesar datos JSON: {str(e)}")
            return jsonify({"error": "Error al procesar la solicitud"}), 400

        if user_input.lower() == "salir":
            return jsonify({"response": "¡Adiós!"})

        # Procesar con Walli
        try:
            walli = Walli(usuario_id)
            response_text = walli.obtener_respuesta_con_resumen(user_input)
            logger.debug(f"Respuesta generada: {response_text}")
            
            return jsonify({"response": response_text})

        except Exception as e:
            logger.error(f"Error al procesar respuesta: {str(e)}")
            return jsonify({"error": "Error al generar respuesta"}), 500

    except Exception as e:
        logger.error(f"Error general: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500


@bp.route('/chat_history')
def get_chat_history():
    return jsonify({"history": chat_history})