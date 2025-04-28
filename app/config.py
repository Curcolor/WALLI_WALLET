import os
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave-secreta-por-defecto')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'lunarspace')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'walli_database')
    PORT = int(os.getenv('PORT', 5050))
    HOST = os.getenv('HOST', '0.0.0.0')
    LOGIN_VIEW = 'auth.login'
    DEEPSEEK_API_KEY = 'sk-ae7619ef9e324719b65586e0def1e610'