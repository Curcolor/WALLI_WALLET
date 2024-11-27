from flask import Blueprint, request, jsonify, session
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

@bp.route('/crear', methods=['POST'])
def crear_pago():
    try:
        datos = request.get_json()
        
        # Validar que los datos necesarios estén presentes
        if not all(key in datos for key in ['cuenta_id', 'servicio_id', 'monto']):
            return jsonify({'error': 'Faltan datos requeridos'}), 400
            
        # Convertir el monto a float
        try:
            monto = float(datos['monto'])
        except ValueError:
            return jsonify({'error': 'El monto debe ser un número válido'}), 400

        pago_id = PagoServicio.crear_pago(
            cuenta_id=datos['cuenta_id'],
            servicio_id=datos['servicio_id'],
            monto=monto
        )
        
        return jsonify({
            'mensaje': 'Pago realizado exitosamente',
            'pago_id': pago_id
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error en crear_pago: {str(e)}")  # Para debugging
        return jsonify({'error': 'Error al procesar el pago'}), 500