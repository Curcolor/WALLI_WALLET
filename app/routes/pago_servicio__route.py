from flask import Blueprint, request, jsonify, render_template, session
from app.models.pago_servicio import PagoServicio

bp = Blueprint('pago_servicio', __name__, url_prefix='/api/pago-servicio')

@bp.route('/listar', methods=['GET'])
def listar_pagos():
    try:
        # Obtener el ID del cliente de la sesión
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'error': 'No autorizado'}), 401

        pagos = PagoServicio.obtener_pagos_por_cliente(cliente_id)
        return jsonify({'pagos': pagos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/crear', methods=['GET', 'POST'])
def crear_pago():
    if request.method == 'GET':
        return render_template('pago_servicio/crear.html')
        
    # Si es POST
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