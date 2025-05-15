from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.cuenta_service import CuentaService
from app.services.servicio_service import ServicioService
from app.schemas.servicio_schema import ServicioSchema

bp = Blueprint('pago_servicio', __name__, url_prefix='/api/pago-servicio')

@bp.route('/listar', methods=['GET'])
@login_required
def listar_pagos():
    try:
        pagos = CuentaService.obtener_pagos_por_cliente(current_user.id_cuenta)
        return jsonify({'pagos': pagos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/servicios', methods=['GET'])
@login_required
def listar_servicios():
    try:
        servicios = ServicioService.get_all_servicios()
        schema = ServicioSchema(many=True)
        return jsonify(schema.dump(servicios))
    except Exception as e:
        print(f"Error al obtener servicios: {str(e)}")
        return jsonify({'error': 'Error al obtener los servicios'}), 500

@bp.route('/crear', methods=['POST'])
@login_required
def crear_pago():
    try:
        data = request.get_json()
        servicio_id = int(data.get('servicio_id', 0))
        monto = float(data.get('monto', 0))
        referencia = data.get('referencia', None)
        
        if servicio_id <= 0 or monto <= 0:
            return jsonify({'error': 'Datos incompletos o inválidos'}), 400
            
        resultado = CuentaService.pagar_servicio(
            cuenta_id=current_user.id_cuenta,
            servicio_id=servicio_id,
            monto=monto,
            referencia=referencia
        )
        
        return jsonify({
            'id_pago': resultado['id_pago'],
            'nuevo_saldo': resultado['nuevo_saldo'],
            'mensaje': 'Pago realizado con éxito'
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error en pago: {str(e)}")
        return jsonify({'error': 'Error al procesar el pago'}), 500