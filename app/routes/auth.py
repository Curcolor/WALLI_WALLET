from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Cliente, Cuenta
from app.forms.auth_forms import LoginForm, RegistroForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            print("Datos del formulario:", form.numero_telefono_ingreso.data, form.clave_ingreso.data)  # Registro de depuración
            cuenta = Cuenta.verificar_login(
                form.numero_telefono_ingreso.data,
                form.clave_ingreso.data
            )
            if cuenta:
                print("Cuenta encontrada:", cuenta)  # Registro de depuración
                cuenta_obj = Cuenta.get(cuenta['id_cuenta'])
                login_user(cuenta_obj)
                return redirect(url_for('viewpages.dashboard'))
            flash('Teléfono o clave incorrectos', 'error')
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('index.html', form=form)

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('viewpages.dashboard'))
    
    form = RegistroForm()
    if form.validate_on_submit():
        try:
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
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('registro.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('viewpages.index'))