from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.services.cuenta_service import CuentaService
from app.schemas.transaccion_resumen_schema import TransaccionResumenSchema

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/recent-transactions', methods=['GET'])
@login_required
def get_recent_transactions():
    try:
        # Obtener las transacciones recientes
        transacciones = CuentaService.obtener_transacciones_recientes(current_user.id_cuenta)
        
        # Serializar con Marshmallow
        schema = TransaccionResumenSchema(many=True)
        result = schema.dump(transacciones)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error al obtener transacciones: {e}")
        return jsonify([])