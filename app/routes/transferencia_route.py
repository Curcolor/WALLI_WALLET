from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.cuenta import Cuenta
from app.models.transaccion import Transaccion

bp = Blueprint('transferencia', __name__, url_prefix='/api/transferencia')

@bp.route('/transferir', methods=['POST'])
@login_required
def transferir():
    try:
        datos = request.get_json()
        
        numero_telefono_destino = datos.get('cuenta_destino')  # Viene del campo recipientAccount del formulario
        monto = float(datos.get('monto', 0))
        descripcion = datos.get('descripcion')
        
        # Validar el número de teléfono
        if not numero_telefono_destino or len(numero_telefono_destino) != 10:
            return jsonify({'error': 'Número de teléfono inválido. Debe tener 10 dígitos'}), 400
            
        if not numero_telefono_destino.isdigit():
            return jsonify({'error': 'El número de teléfono solo debe contener dígitos'}), 400
            
        if monto <= 0:
            return jsonify({'error': 'El monto debe ser positivo'}), 400
        
        if monto < 1000:
            return jsonify({'error': 'El monto mínimo de transferencia es $1.000'}), 400
        
        # Realizar la transferencia usando el número de teléfono
        nuevo_saldo = Cuenta.transferir_dinero(
            cuenta_origen_id=current_user.id,
            numero_telefono_destino=numero_telefono_destino,
            monto=monto,
            descripcion=descripcion
        )
        
        return jsonify({
            'mensaje': 'Transferencia realizada con éxito',
            'monto': monto,
            'nuevo_saldo': nuevo_saldo
        }), 200
        
    except ValueError as e:
        print(f"Error de validación: {str(e)}")  # Debug
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error en transferencia: {str(e)}")  # Debug
        return jsonify({'error': 'Error al procesar la transferencia'}), 500 

@bp.route('/historial', methods=['GET'])
@login_required
def obtener_historial():
    try:
        # Obtener el historial de transacciones del usuario actual
        transacciones = Transaccion.obtener_transacciones_usuario(current_user.id)
        
        # Formatear las transacciones para el frontend
        historial_formateado = []
        for trans in transacciones:
            historial_formateado.append({
                'cuenta_envio': trans[0],
                'monto': float(trans[1]),
                'fecha': trans[2].strftime('%Y-%m-%d %H:%M:%S'),
                'canal': trans[3],
                'estado': trans[4]
            })
        
        return jsonify({
            'transacciones': historial_formateado
        }), 200
        
    except Exception as e:
        print(f"Error al obtener historial: {str(e)}")  # Debug
        return jsonify({'error': 'Error al obtener el historial de transacciones'}), 500 
    