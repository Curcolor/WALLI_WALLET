from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.cuenta_service import CuentaService

bp = Blueprint('transferencia', __name__, url_prefix='/api/transferencia')

@bp.route('/transferir', methods=['POST'])
@login_required
def transferir():
    try:
        data = request.get_json()
        numero_cuenta_destino = data.get('cuenta_destino', '')
        monto = float(data.get('monto', 0))
        descripcion = data.get('descripcion', '')
        
        if not numero_cuenta_destino or monto <= 0:
            return jsonify({'error': 'Datos incompletos o inválidos'}), 400
            
        resultado = CuentaService.realizar_transferencia(
            cuenta_origen_id=current_user.id_cuenta,
            numero_telefono_destino=numero_cuenta_destino,
            monto=monto,
            descripcion=descripcion
        )
        
        return jsonify({
            'id_transferencia': resultado['id_transaccion'],
            'nuevo_saldo': resultado['nuevo_saldo'],
            'mensaje': 'Transferencia realizada con éxito'
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error en transferencia: {str(e)}")
        return jsonify({'error': 'Error al procesar la transferencia'}), 500