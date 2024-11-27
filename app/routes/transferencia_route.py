from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.cuenta import Cuenta

bp = Blueprint('transferencia', __name__, url_prefix='/api/transferencia')

@bp.route('/transferir', methods=['POST'])
@login_required
def transferir():
    try:
        datos = request.get_json()
        print(f"Datos recibidos: {datos}")  # Debug
        
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