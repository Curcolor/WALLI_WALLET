from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.connection_database import get_db_connection

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/recent-transactions', methods=['GET'])
@login_required
def get_recent_transactions():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Obtener el ID de la cuenta del usuario actual
        cursor.execute("""
            SELECT id_cuenta 
            FROM Cuentas 
            WHERE id_cliente = %s
        """, (current_user.id_cliente,))
        cuenta = cursor.fetchone()
        
        if not cuenta:
            return jsonify([])

        # Consultar depósitos
        cursor.execute("""
            SELECT 
                'DEPOSITO' as tipo_transaccion,
                monto,
                fecha_deposito as fecha_transaccion,
                'Depósito realizado' as descripcion,
                estado
            FROM Deposito 
            WHERE id_cuenta = %s
            
            UNION ALL
            
            SELECT 
                'RETIRO' as tipo_transaccion,
                monto,
                fecha_retiro as fecha_transaccion,
                'Retiro de dinero' as descripcion,
                estado
            FROM Retiros 
            WHERE id_cuenta = %s
            
            UNION ALL
            
            SELECT 
                'TRANSFERENCIA' as tipo_transaccion,
                monto,
                fecha_transaccion,
                CASE 
                    WHEN id_cuenta_origen = %s THEN 'Transferencia enviada'
                    ELSE 'Transferencia recibida'
                END as descripcion,
                estado
            FROM Transaccion 
            WHERE id_cuenta_origen = %s OR id_cuenta_envio = %s
            
            UNION ALL
            
            SELECT 
                'SERVICIO' as tipo_transaccion,
                ps.monto,
                ps.fecha_pago as fecha_transaccion,
                CONCAT('Pago de ', IFNULL(s.nombre_servicio, 'servicio')) as descripcion,
                ps.estado
            FROM Pagosservicios ps
            LEFT JOIN Servicios s ON ps.id_servicio = s.id_servicio
            WHERE ps.id_cuenta = %s
            
            ORDER BY fecha_transaccion DESC
            LIMIT 10
        """, (cuenta['id_cuenta'], cuenta['id_cuenta'], cuenta['id_cuenta'], 
              cuenta['id_cuenta'], cuenta['id_cuenta'], cuenta['id_cuenta']))
        
        transactions = cursor.fetchall()
        
        # Formatear fechas para JSON
        for transaction in transactions:
            if transaction['fecha_transaccion']:
                transaction['fecha_transaccion'] = transaction['fecha_transaccion'].strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"Transacciones encontradas: {len(transactions)}")
        for t in transactions:
            print(f"- {t['tipo_transaccion']}: {t['monto']} ({t['fecha_transaccion']}) - {t['estado']}")
            
        return jsonify(transactions)
        
    except Exception as e:
        print(f"Error al obtener transacciones: {e}")
        return jsonify([])
    finally:
        cursor.close()
        conn.close()