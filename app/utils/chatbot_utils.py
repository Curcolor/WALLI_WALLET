import os
import requests
from dotenv import load_dotenv
from app.connection_database import get_db_connection
from app.models import Cliente, Cuenta, Transaccion, Deposito, Retiro, PagoServicio

load_dotenv()

def get_account_info(cliente_id):
    """Obtiene información básica de la cuenta del cliente"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.saldo_actual, cl.nombre, cl.apellido 
            FROM Cuentas c
            JOIN Clientes cl ON c.id_cliente = cl.id_cliente
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
            SELECT t.* FROM Transaccion t
            JOIN Cuentas c ON t.id_cuenta_origen = c.id_cuenta
            WHERE c.id_cliente = %s
            ORDER BY t.fecha_transaccion DESC LIMIT 5
        """, (cliente_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def get_chatbot_response(prompt, cliente_id=None):
    api_key = os.getenv('DEEPSEEK_API_KEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Contexto del sistema con información de la cuenta si está disponible
    system_context = {
        "role": "system",
        "content": """Eres WALLI, un asistente financiero virtual del banco WALLI WALLET. 
        Tu objetivo es ayudar a los clientes con sus consultas financieras y bancarias 
        de manera profesional y amigable. Siempre te refieres a ti mismo como WALLI."""
    }
    
    # Agregar información del cliente si está disponible
    user_context = ""
    if cliente_id:
        try:
            cuenta_info = get_account_info(cliente_id)
            transacciones = get_recent_transactions(cliente_id)
            
            if cuenta_info:
                user_context = f"""
                Cliente: {cuenta_info['nombre']} {cuenta_info['apellido']}
                Saldo actual: ${cuenta_info['saldo_actual']}
                """
                
            if transacciones:
                user_context += "\nÚltimas transacciones:\n"
                for t in transacciones:
                    user_context += f"- ${t['monto']} ({t['fecha_transaccion']})\n"
        except Exception as e:
            print(f"Error al obtener información del cliente: {e}")
    
    url = 'https://api.deepseek.com/v1/chat/completions'
    payload = {
        "model": "deepseek-chat",
        "messages": [
            system_context,
            {"role": "user", "content": f"{user_context}\n\nConsulta del usuario: {prompt}"}
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Lo siento, ha ocurrido un error. Por favor, intenta nuevamente más tarde."