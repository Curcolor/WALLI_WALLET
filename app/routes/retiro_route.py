from flask import Blueprint, request, jsonify, render_template, session
from app.models.retiro import Retiro
from app.models.cuenta import Cuenta
from flask_login import login_required, current_user

bp = Blueprint('retiro', __name__, url_prefix='/api/retiro')

@bp.route('/crear', methods=['GET', 'POST'])
def crear_retiro():
    if request.method == 'GET':
        return render_template('retiro/crear.html')
    
    # Si es POST
    datos = request.get_json()
    try:
        retiro_id = Retiro.crear_retiro(
            cuenta_id=datos['cuenta_id'],
            monto=datos['monto']
        )
        return jsonify({
            'mensaje': 'Retiro realizado exitosamente',
            'retiro_id': retiro_id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error al procesar el retiro'}), 500

@bp.route('/listar', methods=['GET'])
def listar_retiros():
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'error': 'No autorizado'}), 401
            
        retiros = Retiro.obtener_retiros_por_cliente(cliente_id)
        return jsonify({'retiros': retiros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

@bp.route('/retirar', methods=['POST'])
@login_required
def retirar():
    try:
        datos = request.get_json()
        print(f"Datos recibidos: {datos}")  # Debug
        
        monto = float(datos.get('monto', 0))
        cuenta_id = current_user.id
        
        print(f"Procesando retiro - Monto: {monto}, Cuenta ID: {cuenta_id}")  # Debug
        
        if monto <= 0:
            return jsonify({'error': 'El monto debe ser positivo'}), 400
        
        # Obtener saldo antes del retiro
        saldo_anterior = Cuenta.obtener_saldo(cuenta_id)
        print(f"Saldo anterior: {saldo_anterior}")  # Debug
        
        # Realizar el retiro
        nuevo_saldo = Cuenta.retirar_dinero(cuenta_id, monto)
        print(f"Nuevo saldo: {nuevo_saldo}")  # Debug
        
        return jsonify({
            'mensaje': 'Retiro realizado con éxito',
            'monto': monto,
            'nuevo_saldo': nuevo_saldo,
            'saldo_anterior': saldo_anterior
        }), 200
        
    except ValueError as e:
        print(f"Error de validación: {str(e)}")  # Debug
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error en retiro: {str(e)}")  # Debug
        return jsonify({'error': 'Error al procesar el retiro'}), 500 