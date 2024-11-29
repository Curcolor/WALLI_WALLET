from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

load_dotenv()

ENCRYPTION_KEY = b'S1Zla2N6mRYOcoFvQONtsUytpMf0XJC8B9y4pgodcJk='  # Usa la clave con la que encriptaste originalmente

def get_encryption_key():
    try:
        # Usar la clave definida
        return Fernet(ENCRYPTION_KEY)
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