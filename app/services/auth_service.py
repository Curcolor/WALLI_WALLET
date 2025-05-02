from flask import session
from app.models import Cliente, Cuenta
from app.extensions import db
import random
import string
from werkzeug.security import generate_password_hash

class AuthService:
    @staticmethod
    def login(numero_telefono, clave):
        """
        Verifica las credenciales de login y retorna la cuenta si es válida
        """
        cuenta = Cuenta.query.filter_by(numero_telefono_ingreso=numero_telefono).first()
        
        if not cuenta:
            return None
            
        if not cuenta.check_password(clave):
            return None
            
        if cuenta.estado != 'activa':
            raise ValueError("La cuenta no está activa")
            
        return cuenta
        
    @staticmethod
    def register(nombre, apellido, documento_identidad, correo_electronico, 
                fecha_nacimiento, tipo_cuenta, clave_ingreso, numero_telefono_ingreso):
        """
        Registra un nuevo cliente y su cuenta
        """
        # Verificar si ya existe un cliente con ese documento
        cliente_existente = Cliente.query.filter_by(documento_identidad=documento_identidad).first()
        if cliente_existente:
            raise ValueError("Ya existe un cliente con ese documento de identidad")

        # Verificar si ya existe una cuenta con ese teléfono
        cuenta_existente = Cuenta.query.filter_by(numero_telefono_ingreso=numero_telefono_ingreso).first()
        if cuenta_existente:
            raise ValueError("Ya existe una cuenta con ese número de teléfono")
        
        # Crear el cliente
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            documento_identidad=documento_identidad,
            correo_electronico=correo_electronico,
            fecha_nacimiento=fecha_nacimiento
        )
        
        # Crear la cuenta
        cuenta = Cuenta(
            tipo_cuenta=tipo_cuenta,
            clave_ingreso=clave_ingreso,
            numero_telefono_ingreso=numero_telefono_ingreso,
            saldo_actual=0.00,
            estado='activa'
        )
        
        # Relacionar cliente y cuenta
        cliente.cuenta = cuenta
        
        # Guardar en la base de datos
        db.session.add(cliente)
        db.session.commit()
        
        return cliente.id_cliente
        
    @staticmethod
    def logout():
        """
        Elimina las variables de sesión relacionadas con el usuario
        """
        session.pop('_user_id', None)
        return True