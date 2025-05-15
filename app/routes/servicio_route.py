from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.servicio_service import ServicioService
from app.schemas.servicio_schema import ServicioSchema
from app.services.cuenta_service import CuentaService

bp = Blueprint('servicio', __name__, url_prefix='/api/servicio')

@bp.route('/listar', methods=['GET'])
@login_required
def listar_servicios():
    """Lista todos los servicios disponibles"""
    try:
        servicios = ServicioService.get_all_servicios()
        schema = ServicioSchema(many=True)
        result = schema.dump(servicios)
        return jsonify({'servicios': result}), 200
    except Exception as e:
        print(f"Error al listar servicios: {str(e)}")
        return jsonify({'error': str(e)}), 400

@bp.route('/pagar', methods=['POST'])
@login_required
def pagar_servicio():
    """Realiza el pago de un servicio"""
    datos = request.get_json()
    
    try:
        # Usamos la cuenta del usuario autenticado
        resultado = CuentaService.pagar_servicio(
            cuenta_id=current_user.id_cuenta,
            servicio_id=datos['servicio_id'],
            monto=datos['monto'],
            referencia=datos.get('referencia')
        )
        
        return jsonify({
            'mensaje': 'Pago realizado exitosamente',
            'pago_id': resultado['id_pago'],
            'nuevo_saldo': resultado['nuevo_saldo']
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error al procesar pago: {str(e)}")
        return jsonify({'error': 'Error al procesar el pago'}), 500