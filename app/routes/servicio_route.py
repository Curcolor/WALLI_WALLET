from flask import Blueprint, request, jsonify
from app.models.servicio import Servicio
from app.models.pago_servicio import PagoServicio

bp = Blueprint('servicio', __name__, url_prefix='/api/servicio')

@bp.route('/listar', methods=['GET'])
def listar_servicios():
    try:
        servicios = Servicio.obtener_servicios()
        return jsonify({'servicios': servicios}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/pagar', methods=['POST'])
def pagar_servicio():
    datos = request.get_json()
    
    try:
        pago_id = PagoServicio.crear_pago(
            cuenta_id=datos['cuenta_id'],
            servicio_id=datos['servicio_id'],
            monto=datos['monto']
        )
        return jsonify({
            'mensaje': 'Pago realizado exitosamente',
            'pago_id': pago_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al procesar el pago'}), 500 