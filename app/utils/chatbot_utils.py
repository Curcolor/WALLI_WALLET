import os
import requests
from dotenv import load_dotenv
from app.connection_database import get_db_connection
from app.models import Cliente, Cuenta, transaccion, deposito, Retiro, PagoServicio
import json

load_dotenv()

def format_money(amount):
    return f"${amount:,.2f}"

def get_account_info(cliente_id):
    """Obtiene información básica de la cuenta del cliente"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.saldo_actual, cl.nombre, cl.apellido 
            FROM cuentas c
            JOIN clientes cl ON c.id_cliente = cl.id_cliente
            WHERE cl.id_cliente = %s
        """, (cliente_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def get_recent_transactions(cliente_id):
    """Obtiene las últimas transacciones del cliente"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT t.* FROM transaccion t
            JOIN cuentas c ON t.id_cuenta_origen = c.id_cuenta
            WHERE c.id_cliente = %s
            ORDER BY t.fecha_transaccion DESC LIMIT 5
        """, (cliente_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_financial_context(cliente_id):
    """Obtiene y formatea la información financiera del cliente"""
    try:
        account_info = get_account_info(cliente_id)
        transactions = get_recent_transactions(cliente_id)
        
        if not account_info:
            return "No se encontró información de la cuenta."

        # Formatear la información de manera segura y estructurada
        context = {
            "nombre_cliente": f"{account_info['nombre']} {account_info['apellido']}",
            "saldo": format_money(account_info['saldo_actual']),
            "ultimas_transacciones": []
        }

        if transactions:
            for t in transactions:
                context["ultimas_transacciones"].append({
                    "monto": format_money(t['monto']),
                    "fecha": t['fecha_transaccion'].strftime("%d/%m/%Y"),
                    "tipo": t['tipo_transaccion']
                })

        return context
    except Exception as e:
        print(f"Error al obtener contexto financiero: {e}")
        return None

def get_chatbot_response(prompt, cliente_id=None):
    api_key = os.getenv('DEEPSEEK_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Obtener contexto financiero
    financial_context = get_financial_context(cliente_id) if cliente_id else None
    
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
    except Exception as e:
        return "Lo siento, ha ocurrido un error. Por favor, intenta nuevamente más tarde."