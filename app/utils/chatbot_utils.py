import os
import requests
from dotenv import load_dotenv
from app.services.cuenta_service import CuentaService
from app.schemas.transaccion_resumen_schema import TransaccionResumenSchema
from app.extensions import db
import json

load_dotenv()

def format_money(amount):
    """Formatea un valor monetario con formato de moneda"""
    if amount is None:
        return "$0.00"
    return f"${float(amount):,.2f}"

def get_account_info(cuenta_id):
    """Obtiene información básica de la cuenta usando el servicio existente"""
    try:
        # Usar el servicio que ya tienes implementado
        return CuentaService.get_info_cuenta(cuenta_id)
    except Exception as e:
        print(f"Error al obtener información de la cuenta: {e}")
        return None

def get_recent_transactions(cuenta_id, limit=5):
    """Obtiene las transacciones recientes usando el servicio existente"""
    try:
        # Usar el servicio que ya tienes implementado
        transactions = CuentaService.obtener_transacciones_recientes(cuenta_id, limit)
        
        # Como el servicio devuelve objetos de SQLAlchemy Row, los convertimos a diccionarios
        schema = TransaccionResumenSchema(many=True)
        return schema.dump(transactions)
    except Exception as e:
        print(f"Error al obtener transacciones recientes: {e}")
        return []

def get_financial_context(cuenta_id):
    """Obtiene y formatea la información financiera del cliente usando servicios"""
    try:
        account_info = get_account_info(cuenta_id)
        transactions = get_recent_transactions(cuenta_id)
        
        if not account_info:
            return "No se encontró información de la cuenta."

        # Formatear la información de manera segura y estructurada
        context = {
            "nombre_cliente": account_info['nombre_usuario'],
            "saldo": format_money(account_info['saldo_actual']),
            "ultimas_transacciones": []
        }

        if transactions:
            for t in transactions:
                context["ultimas_transacciones"].append({
                    "monto": format_money(t['monto']),
                    "fecha": t['fecha_transaccion'].strftime("%d/%m/%Y") if hasattr(t['fecha_transaccion'], 'strftime') else t['fecha_transaccion'],
                    "tipo": t['tipo_transaccion']
                })

        return context
    except Exception as e:
        print(f"Error al obtener contexto financiero: {e}")
        return None

def get_chatbot_response(prompt, cuenta_id=None):
    api_key = os.getenv('API_DEEPSEEK_KEY')
    if not api_key:
        return "Error de configuración: No se encontró la clave API."
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Obtener contexto financiero
    financial_context = get_financial_context(cuenta_id) if cuenta_id else None
    
    # Crear el mensaje del sistema
    system_message = """Eres WALLI, el asistente financiero virtual de WALLI WALLET. 
    Responde de manera profesional y amigable, siempre refiriéndote a ti mismo como WALLI.
    Puedes usar la información financiera proporcionada para dar respuestas personalizadas,
    pero NUNCA muestres datos sensibles directamente. En su lugar, usa la información
    para contextualizar tus respuestas."""

    # Crear el mensaje del usuario con contexto
    user_message = prompt
    if financial_context:
        context_prompt = f"""
        [Contexto interno - NO mostrar directamente]:
        Cliente: {financial_context['nombre_cliente']}
        Saldo actual: {financial_context['saldo']}
        Número de transacciones recientes: {len(financial_context['ultimas_transacciones'])}
        """
        user_message = f"{context_prompt}\n\nConsulta del usuario: {prompt}"

    url = 'https://api.deepseek.com/v1/chat/completions'
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.5,
        "max_tokens": 200,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"Error de autenticación con la API: {e}")
            return "Lo siento, hay un problema de autenticación con el servicio. Por favor, contacta al soporte técnico."
        else:
            print(f"Error de la API: {e}")
            return "Lo siento, ha ocurrido un error con el servicio. Por favor, intenta nuevamente más tarde."
    except Exception as e:
        print(f"Error al obtener respuesta del chatbot: {e}")
        return "Lo siento, ha ocurrido un error inesperado. Por favor, intenta nuevamente más tarde."