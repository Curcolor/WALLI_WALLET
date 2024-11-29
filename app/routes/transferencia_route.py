from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models.transaccion import Transaccion
from app.utils.encryption import get_encryption_key

bp = Blueprint('transferencia', __name__, url_prefix='/api/transferencia')

@bp.route('/transferir', methods=['POST'])
@login_required
def transferir():
    try:
        datos = request.get_json()
        print("Datos recibidos:", datos)  # Debug
        
        if not datos:
            return jsonify({'error': 'No se recibieron datos'}), 400
            
        numero_telefono_destino = datos.get('cuenta_destino')
        print("Número destino:", numero_telefono_destino)  # Debug
        
        try:
            monto = float(datos.get('monto', 0))
        except ValueError:
            return jsonify({'error': 'El monto debe ser un número válido'}), 400
            
        descripcion = datos.get('descripcion')
        
        # Validar el número de teléfono
        if not numero_telefono_destino:
            return jsonify({'error': 'El número de teléfono es requerido'}), 400
            
        if len(numero_telefono_destino) != 10:
            return jsonify({'error': f'Número de teléfono inválido. Debe tener 10 dígitos. Recibido: {len(numero_telefono_destino)} dígitos'}), 400
            
        if not numero_telefono_destino.isdigit():
            return jsonify({'error': 'El número de teléfono solo debe contener dígitos'}), 400
            
        if monto <= 0:
            return jsonify({'error': 'El monto debe ser positivo'}), 400
        
        if monto < 1000:
            return jsonify({'error': 'El monto mínimo de transferencia es $1.000'}), 400
            
        print(f"Usuario actual ID: {current_user.id}")  # Debug
        
        nuevo_saldo = Transaccion.transferir_dinero(
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