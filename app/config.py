import os
from datetime import timedelta
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

class Config:
    # Configuración básica de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.environ.get('MYSQL_USER')}:"
        f"{os.environ.get('MYSQL_PASSWORD')}@"
        f"{os.environ.get('MYSQL_HOST')}/"
        f"{os.environ.get('MYSQL_DATABASE')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Clave de encriptación para los datos sensibles
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    
    # Clave API para DeepSeek
    API_DEEPSEEK_KEY = os.environ.get('API_DEEPSEEK_KEY')
    
    @staticmethod
    def init_app(app):
        """Inicialización adicional de la aplicación"""
        pass

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False

class TestingConfig(Config):
    """Configuración para entorno de pruebas"""
    TESTING = True
    # Usar una base de datos SQLite en memoria para pruebas
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Diccionario de configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}