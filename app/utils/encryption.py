from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
from base64 import b64encode, b64decode

load_dotenv()

def get_encryption_key():
    # Primero intenta obtener la llave del entorno
    env_key = os.getenv('ENCRYPTION_KEY')
    if env_key:
        return Fernet(env_key.encode())
    
    # Si no existe en el entorno, usa el archivo como respaldo
    key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'encryption.key')
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
    return Fernet(key)

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