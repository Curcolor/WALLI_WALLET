from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

load_dotenv()

def get_encryption_key():
    try:
        # Intenta obtener la clave del entorno
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            print("ADVERTENCIA: No se encontró ENCRYPTION_KEY en variables de entorno")
            # Si no existe, crea una nueva (esto debería ocurrir solo en desarrollo)
            key = Fernet.generate_key()
            print(f"Nueva clave generada: {key}")  # Debug - NO DEJAR EN PRODUCCIÓN
        
        return Fernet(key if isinstance(key, bytes) else key.encode())
    except Exception as e:
        print(f"Error al obtener clave de encriptación: {str(e)}")
        raise

# Instancia global de Fernet
fernet = get_encryption_key()

def encrypt_data(data):
    if not data:
        return None
    return b64encode(fernet.encrypt(str(data).encode())).decode()

def decrypt_data(encrypted_data):
    if not encrypted_data:
        return None
    try:
        return fernet.decrypt(b64decode(encrypted_data)).decode()
    except:
        return None 