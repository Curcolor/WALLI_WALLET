from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, login_required, current_user
from app.forms.auth_forms import LoginForm, RegistroForm
from app.models import Cuenta, Cliente
from app.connection_database import get_db_connection
from ..utils.chatbot_utils import get_chatbot_response

bp = Blueprint('viewpages', __name__)

def obtener_info_cuenta(id_cuenta):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT c.saldo_actual, cl.nombre, cl.apellido
            FROM cuentas c
            JOIN clientes cl ON c.id_cliente = cl.id_cliente
            WHERE c.id_cuenta = %s
        """, (id_cuenta,))
        
        cuenta_info = cursor.fetchone()
        print("Datos obtenidos de la BD:", cuenta_info)  # Debug
        if cuenta_info:
            info = {
                'nombre_usuario': f"{cuenta_info['nombre']} {cuenta_info['apellido']}",
                'saldo_actual': float(cuenta_info['saldo_actual'])
            }
            print("Info procesada:", info)  # Debug
            return info
        return {
            'nombre_usuario': 'Usuario',
            'saldo_actual': 0.0
        }
    finally:
        cursor.close()
        conn.close()

def obtener_saldo_actual(id_cuenta):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT saldo_actual FROM cuentas WHERE id_cuenta = %s", (id_cuenta,))
        resultado = cursor.fetchone()
        return float(resultado['saldo_actual']) if resultado else 0.0
    finally:
        cursor.close()
        conn.close()

@bp.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            numero_telefono = form.numero_telefono_ingreso.data
            clave = form.clave_ingreso.data
            print(f"Intentando login con: {numero_telefono}")  # Debug
            
            cuenta = Cuenta.verificar_login(numero_telefono, clave)
            if cuenta:
                print(f"Login exitoso para cuenta: {cuenta}")  # Debug
                cuenta_obj = Cuenta.get(cuenta['id_cuenta'])
                if cuenta_obj:
                    login_user(cuenta_obj)
                    return redirect(url_for('viewpages.dashboard'))
                else:
                    print("No se pudo crear el objeto cuenta")  # Debug
                    flash('Error al cargar la cuenta', 'error')
            else:
                print("Verificación de login falló")  # Debug
                flash('Teléfono o clave incorrectos', 'error')
        except Exception as e:
            print(f"Error en login: {str(e)}")  # Debug
            flash(str(e), 'error')
    
    return render_template('index.html', form=form)

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        try:
            # Crear el cliente y la cuenta en una sola operación
            cliente_id = Cliente.crear_cliente_con_cuenta(
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                documento_identidad=form.documento_identidad.data,
                correo_electronico=form.correo_electronico.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                tipo_cuenta=form.tipo_cuenta.data,
                clave_ingreso=form.clave_ingreso.data,
                numero_telefono_ingreso=form.numero_telefono_ingreso.data
            )
            
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('viewpages.index'))
            
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('registro.html', form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    try:
        info_cuenta = obtener_info_cuenta(current_user.id)
        print("Info cuenta en dashboard:", info_cuenta)  # Debug
        return render_template('dashboard.html', **info_cuenta)
    except Exception as e:
        print(f"Error al cargar dashboard: {str(e)}")  # Debug
        flash('Error al cargar los datos del dashboard', 'error')
        return redirect(url_for('viewpages.index'))

@bp.route('/depositar')
@login_required
def depositar():
    if not current_user.is_authenticated:
        return redirect(url_for('viewpages.index'))
    
    info_cuenta = obtener_info_cuenta(current_user.id)
    return render_template('depositar_new.html', **info_cuenta)

@bp.route('/retirar')
@login_required
def retirar():
    if not current_user.is_authenticated:
        return redirect(url_for('viewpages.index'))
    
    info_cuenta = obtener_info_cuenta(current_user.id)
    return render_template('retirar_new.html', **info_cuenta)

@bp.route('/transferir')
@login_required
def transferir():
    if not current_user.is_authenticated:
        return redirect(url_for('viewpages.index'))
    
    info_cuenta = obtener_info_cuenta(current_user.id)
    return render_template('transferir_new.html', **info_cuenta)

@bp.route('/servicios')
@login_required
def servicios():
    try:
        info_cuenta = obtener_info_cuenta(current_user.id)
        print("Info cuenta:", info_cuenta)  # Debug para ver qué datos llegan
        return render_template('servicios_new.html', **info_cuenta)
    except Exception as e:
        print(f"Error al cargar servicios: {str(e)}")
        flash('Error al cargar la página de servicios', 'error')
        return redirect(url_for('viewpages.dashboard'))
    
@bp.route('/pago-servicios')
@login_required
def pago_servicios():
    servicio_id = request.args.get('servicio_id', '')
    
    # Usar current_user en lugar de session
    info_cuenta = obtener_info_cuenta(current_user.id)
    
    return render_template('pago_servicios.html',
                         nombre_usuario=info_cuenta['nombre_usuario'],
                         saldo_actual=info_cuenta['saldo_actual'],
                         servicio_id=servicio_id)
@bp.route('/chatbot')
@login_required
def chatbot():
    info_cuenta = obtener_info_cuenta(current_user.id)
    return render_template('chatbot.html', **info_cuenta)

@bp.route('/chatbot/message', methods=['POST'])
@login_required
def chatbot_message():
    try:
        data = request.json
        user_message = data.get('message', '')
        cliente_id = current_user.id_cliente if current_user.is_authenticated else None
        
        bot_response = get_chatbot_response(user_message, cliente_id)
        return jsonify({
            'success': True,
            'response': bot_response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'response': 'Lo siento, ocurrió un error al procesar tu solicitud.'
        }), 500
