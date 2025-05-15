from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
import logging
from werkzeug.exceptions import BadRequest
from app.utils.chatbot_utils import get_chatbot_response

bp = Blueprint('walli', __name__, url_prefix='/api/walli')

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@bp.route('/send', methods=['POST'])
@login_required
def send_message():
    logger.debug("Iniciando procesamiento de mensaje...")
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            raise BadRequest('No message provided')
        
        logger.debug(f"Usuario autenticado con ID: {current_user.id_cuenta}")
        logger.debug(f"Mensaje recibido: {user_input}")
        
        # Ahora pasamos el ID de la cuenta directamente
        response_text = get_chatbot_response(user_input, current_user.id_cuenta)
        
        return jsonify({
            'status': 'success',
            'response': response_text
        })
    except Exception as e:
        logger.error(f"Error al procesar respuesta: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error al procesar la solicitud'
        }), 500

@bp.route('/chat_history')
@login_required
def get_chat_history():
    # Esta parte podría usar un servicio para obtener el historial del chat
    # desde una base de datos si decides implementarlo así
    # Por ahora retornamos un arreglo vacío
    return jsonify({"history": []})