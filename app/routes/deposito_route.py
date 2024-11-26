from flask import Blueprint, request, jsonify, current_app, session
from flask_login import current_user, login_required
from app.models.deposito import Deposito
from app.connection_database import get_db_connection

bp = Blueprint('deposito', __name__, url_prefix='/api/deposito')

@bp.route('/crear', methods=['POST'])
@login_required
def crear_deposito():
    try:
        datos = request.get_json()
        monto = float(datos.get('monto', 0))
        
        if monto < 1000:
            return jsonify({'error': 'El monto mínimo de depósito es $1.000'}), 400
            
        deposito_id = Deposito.crear_deposito(
            id_cuenta=current_user.id,
            monto=monto
        )
        
        # Obtener el nuevo saldo después del depósito
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT saldo_actual FROM Cuentas WHERE id_cuenta = %s
        """, (current_user.id,))
        nuevo_saldo = cursor.fetchone()['saldo_actual']
        cursor.close()
        conn.close()
        
        return jsonify({
            'mensaje': 'Depósito realizado exitosamente',
            'deposito_id': deposito_id,
            'nuevo_saldo': float(nuevo_saldo)
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error en depósito: {str(e)}")
        return jsonify({'error': 'Error al procesar el depósito'}), 500

@bp.route('/listar', methods=['GET'])
def listar_depositos():
    try:
        cliente_id = session.get('cliente_id')
        if not cliente_id:
            return jsonify({'error': 'No autorizado'}), 401
            
        depositos = Deposito.obtener_depositos_por_cliente(cliente_id)
        return jsonify({'depositos': depositos}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 