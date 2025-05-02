from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, login_required, current_user
from app.forms.auth_forms import LoginForm, RegistroForm
from app.models import Cliente
from app.services.cuenta_service import CuentaService
from ..utils.chatbot_utils import get_chatbot_response

bp = Blueprint('viewpages', __name__)

@bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    
    form = LoginForm()
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
        info_cuenta = CuentaService.get_info_cuenta(current_user.id_cuenta)
        if not info_cuenta:
            flash('Error al cargar los datos del dashboard', 'error')
            return redirect(url_for('viewpages.index'))
            
        return render_template('dashboard.html', **info_cuenta)
    except Exception as e:
        print(f"Error al cargar dashboard: {str(e)}")
        flash('Error al cargar los datos del dashboard', 'error')
        return redirect(url_for('viewpages.index'))

@bp.route('/depositar')
@login_required
def depositar():
    info_cuenta = CuentaService.get_info_cuenta(current_user.id_cuenta)
    return render_template('depositar_new.html', **info_cuenta)

@bp.route('/retirar')
@login_required
def retirar():
    info_cuenta = CuentaService.get_info_cuenta(current_user.id_cuenta)
    return render_template('retirar_new.html', **info_cuenta)

@bp.route('/transferir')
@login_required
def transferir():
    info_cuenta = CuentaService.get_info_cuenta(current_user.id_cuenta)
    return render_template('transferir_new.html', **info_cuenta)

@bp.route('/servicios')
@login_required
def servicios():
    info_cuenta = CuentaService.get_info_cuenta(current_user.id_cuenta)
    return render_template('servicios_new.html', **info_cuenta)

@bp.route('/pago-servicios')
@login_required
def pago_servicios():
    servicio_id = request.args.get('servicio_id', '')
    
    # Usar current_user en lugar de session
    info_cuenta = CuentaService.get_info_cuenta(current_user.id_cuenta)
    
    return render_template('pago_servicios.html',
                         nombre_usuario=info_cuenta['nombre_usuario'],
                         saldo_actual=info_cuenta['saldo_actual'],
                         servicio_id=servicio_id)

@bp.route('/chatbot')
@login_required
def chatbot():
    info_cuenta = CuentaService.get_info_cuenta(current_user.id_cuenta)
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
