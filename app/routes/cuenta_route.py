from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.services.cuenta_service import CuentaService

bp = Blueprint('cuenta', __name__, url_prefix='/api/cuenta')

@bp.route('/saldo', methods=['GET'])
@login_required
def obtener_saldo():
    try:
        saldo = CuentaService.obtener_saldo(current_user.id_cuenta)
        return jsonify({'saldo': saldo}), 200
    except Exception as e:
        print(f"Error al obtener saldo: {str(e)}")  # Debug
        return jsonify({'error': 'Error al obtener el saldo'}), 500

@bp.route('/info', methods=['GET'])
@login_required
def obtener_info_cuenta():
    try:
        info = CuentaService.get_info_cuenta(current_user.id_cuenta)
        if info:
            return jsonify(info), 200
        else:
            return jsonify({'error': 'Cuenta no encontrada'}), 404
    except Exception as e:
        print(f"Error al obtener info: {str(e)}")
        return jsonify({'error': 'Error al obtener información'}), 500