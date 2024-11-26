from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, Regexp

class LoginForm(FlaskForm):
    numero_telefono_ingreso = StringField('Número de Teléfono', 
        validators=[
            DataRequired(message="El número de teléfono es requerido"),
            Length(min=10, max=10, message="El número debe tener 10 dígitos"),
            Regexp(r'^\d{10}$', message="Solo se permiten números")
        ])
    
    clave_ingreso = PasswordField('Contraseña', 
        validators=[
            DataRequired(message="La clave es requerida"),
            Length(min=4, max=4, message="La clave debe tener 4 dígitos"),
            Regexp(r'^\d{4}$', message="Solo se permiten números")
        ])

class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', 
        validators=[DataRequired(message="El nombre es requerido")])
    
    apellido = StringField('Apellido', 
        validators=[DataRequired(message="El apellido es requerido")])
    
    documento_identidad = StringField('Documento de Identidad',
        validators=[
            DataRequired(message="El documento de identidad es requerido"),
            Length(min=10, max=10, message="El documento debe tener 10 dígitos"),
            Regexp(r'^\d{10}$', message="Solo se permiten números")
        ])
    
    correo_electronico = StringField('Correo Electrónico',
        validators=[
            DataRequired(message="El correo electrónico es requerido"),
            Regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message="Por favor ingrese un correo electrónico válido")
        ])
    
    fecha_nacimiento = DateField('Fecha de Nacimiento',
        validators=[DataRequired(message="La fecha de nacimiento es requerida")])
    
    tipo_cuenta = SelectField('Tipo de Cuenta',
        choices=[
            ('ahorro', 'Ahorro'),
            ('corriente', 'Corriente'),
            ('cats', 'CATS')
        ],
        validators=[DataRequired(message="Seleccione un tipo de cuenta")])
    
    numero_telefono_ingreso = StringField('Teléfono de Ingreso',
        validators=[
            DataRequired(message="El número de teléfono es requerido"),
            Length(min=10, max=10, message="El teléfono debe tener 10 dígitos"),
            Regexp(r'^\d{10}$', message="Solo se permiten números")
        ])
    
    clave_ingreso = PasswordField('Clave de Ingreso',
        validators=[
            DataRequired(message="La clave es requerida"),
            Length(min=4, max=4, message="La clave debe tener 4 dígitos"),
            Regexp(r'^\d{4}$', message="Solo se permiten números")
        ]) 