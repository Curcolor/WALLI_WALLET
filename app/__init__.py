from flask import Flask
from app.config import Config
from app.routes import blueprints
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'viewpages.index'
login_manager.login_message = 'Por favor inicia sesión para acceder.'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar Flask-Login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Cuenta
        return Cuenta.get(user_id)

    # Registrar blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app