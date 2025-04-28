from flask import Blueprint, jsonify, request, session
from flask_login import login_required, current_user
import logging
from werkzeug.exceptions import BadRequest
# Importar la función get_chatbot_response en lugar de la clase Walli
from app.utils.chatbot_utils import get_chatbot_response

bp = Blueprint('walli', __name__, url_prefix='/api/walli')

chat_history = []

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@bp.route('/send', methods=['POST'])
@login_required  # Esto asegura que el usuario esté autenticado
def send_message():
    logger.debug("Iniciando procesamiento de mensaje...")
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            raise BadRequest('No message provided')
        
        logger.debug(f"Usuario autenticado con ID: {current_user.id}")
        logger.debug(f"Mensaje recibido: {user_input}")
        
        # Usar la función get_chatbot_response en lugar de la clase Walli
        response_text = get_chatbot_response(user_input, current_user.id)
        
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
def get_chat_history():
    return jsonify({"history": chat_history})