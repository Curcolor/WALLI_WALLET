python -m venv venv # Crea un nuevo entorno virtual
pip install -r requirements.txt # Instala todas las dependencias
source venv/Scripts/activate # Activa el entorno virtual
net start MySQL80 # Inicia el servidor MySQL
python run.py # Ejecuta la aplicación Flask