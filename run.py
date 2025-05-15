from app import create_app
import os

# Determinar el entorno de ejecución
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])