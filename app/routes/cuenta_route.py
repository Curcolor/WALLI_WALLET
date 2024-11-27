from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models.cuenta import Cuenta

bp = Blueprint('cuenta', __name__, url_prefix='/api/cuenta')

@bp.route('/saldo', methods=['GET'])
@login_required
def obtener_saldo():
    try:
        saldo = Cuenta.obtener_saldo(current_user.id)
        return jsonify({'saldo': saldo}), 200
    except Exception as e:
        print(f"Error al obtener saldo: {str(e)}")  # Debug
        return jsonify({'error': 'Error al obtener el saldo'}), 500 