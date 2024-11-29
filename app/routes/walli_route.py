from app.chatWalli.walli import Walli
from flask import Blueprint, jsonify, request, session

bp = Blueprint('walli', __name__, url_prefix='/api/walli')

chat_history = []


@bp.route('/send', methods=['POST'])
def send_message():
    user_input = request.form['message']
    if user_input.lower() == "salir":
        return jsonify({"message": "Adios!"})
    
    # Agrega la entrada del usuario al historial
    chat_history.append(f"Tú: {user_input}")

    walli = Walli(session['usuario_id'])
    # Genera y muestra la respuesta palabra por palabra
    response_text = walli.obtener_respuesta_con_resumen(user_input)
    for word in response_text.split():
        chat_history.append(f"Walli: {word}")
    
    return jsonify({"response": response_text})


@bp.route('/chat_history')
def get_chat_history():
    return jsonify({"history": chat_history})