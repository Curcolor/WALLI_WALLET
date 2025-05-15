from flask import session
from app.models import Cliente, Cuenta
from app.extensions import db
from sqlalchemy import or_
from app.utils.encryption import encrypt_data, decrypt_data

class AuthService:
    @staticmethod
    def login(numero_telefono, clave):
        """
        Verifica las credenciales de login y retorna la cuenta si es válida
        """
        # Estrategia 1: Obtener todas las cuentas y comparar el número desencriptado
        cuentas = Cuenta.query.all()
        cuenta_encontrada = None
        
        for cuenta in cuentas:
            try:
                if cuenta.numero_telefono_ingreso == numero_telefono:
                    cuenta_encontrada = cuenta
                    break
            except:
                # Si hay error al desencriptar, continuar con la siguiente
                continue
        
        if not cuenta_encontrada:
            return None
            
        if not cuenta_encontrada.check_password(clave):
            return None
            
        if cuenta_encontrada.estado != 'activa':
            raise ValueError("La cuenta no está activa")
            
        return cuenta_encontrada
        
    @staticmethod
    def register(nombre, apellido, documento_identidad, correo_electronico, 
                fecha_nacimiento, tipo_cuenta, clave_ingreso, numero_telefono_ingreso):
        """
        Registra un nuevo cliente y su cuenta
        """
        # Verificar si ya existe un cliente con ese documento
        # Esto es más complejo con datos encriptados, hay que revisar todos los clientes
        clientes = Cliente.query.all()
        for cliente in clientes:
            try:
                if cliente.documento_identidad == documento_identidad:
                    raise ValueError("Ya existe un cliente con ese documento de identidad")
            except:
                continue
                
        # Verificar si ya existe una cuenta con ese teléfono
        cuentas = Cuenta.query.all()
        for cuenta in cuentas:
            try:
                if cuenta.numero_telefono_ingreso == numero_telefono_ingreso:
                    raise ValueError("Ya existe una cuenta con ese número de teléfono")
            except:
                continue
        
        # Crear el cliente
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            documento_identidad=documento_identidad,  # Se encripta automáticamente 
            correo_electronico=correo_electronico,    # Se encripta automáticamente
            fecha_nacimiento=fecha_nacimiento
        )
        
        # Crear la cuenta
        cuenta = Cuenta(
            tipo_cuenta=tipo_cuenta,
            clave_ingreso=clave_ingreso,              # Se hashea automáticamente
            numero_telefono_ingreso=numero_telefono_ingreso,  # Se encripta automáticamente
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