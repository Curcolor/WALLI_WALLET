from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.services.deposito_service import DepositoService
from app.schemas.deposito_schema import DepositoSchema

bp = Blueprint('deposito', __name__, url_prefix='/api/deposito')

@bp.route('/crear', methods=['POST'])
@login_required
def crear_deposito():
    try:
        data = request.get_json()
        monto = float(data.get('monto', 0))
        
        if monto <= 0:
            return jsonify({'error': 'El monto debe ser mayor a cero'}), 400
            
        deposito = DepositoService.crear_deposito(
            cuenta_id=current_user.id_cuenta,
            monto=monto
        )
        
        schema = DepositoSchema()
        result = schema.dump(deposito)
        
        return jsonify({
            'deposito': result,
            'mensaje': 'Depósito realizado con éxito'
        }), 201
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error en depósito: {str(e)}")
        return jsonify({'error': 'Error al procesar el depósito'}), 500

@bp.route('/historial', methods=['GET'])
@login_required
def historial_depositos():
    try:
        depositos = DepositoService.obtener_depositos_por_cuenta(current_user.id_cuenta)
        
        schema = DepositoSchema(many=True)
        result = schema.dump(depositos)
        
        return jsonify(result)
    except Exception as e:
        print(f"Error al obtener historial: {str(e)}")
        return jsonify({'error': 'Error al obtener el historial de depósitos'}), 500