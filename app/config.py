import os
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
    PORT = int(os.getenv('PORT', 5050))
    HOST = os.getenv('HOST', '0.0.0.0')
    LOGIN_VIEW = 'auth.login'
    DEEPSEEK_API_KEY = os.getenv('API_DEEPSEEK_KEY')