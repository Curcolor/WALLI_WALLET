from app.models import Cuenta, Deposito
from app.extensions import db
from decimal import Decimal

class DepositoService:
    @staticmethod
    def crear_deposito(cuenta_id, monto, canal='web'):
        """
        Crea un nuevo depósito y actualiza el saldo de la cuenta
        """
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
            
        if cuenta.estado != 'activa':
            raise ValueError("La cuenta no está activa")
        
        # Crear el depósito
        deposito = Deposito(
            id_cuenta=cuenta_id,
            monto=monto,
            canal=canal,
            estado='completado'
        )
        
        # Actualizar saldo
        cuenta.saldo_actual = float(cuenta.saldo_actual) + float(monto)
        
        db.session.add(deposito)
        db.session.commit()
        
        return deposito
    
    @staticmethod
    def obtener_depositos_por_cuenta(cuenta_id):
        """
        Obtiene todos los depósitos de una cuenta
        """
        return Deposito.query.filter_by(id_cuenta=cuenta_id).order_by(Deposito.fecha_deposito.desc()).all()
    
    @staticmethod
    def obtener_deposito(deposito_id):
        """
        Obtiene un depósito específico
        """
        return Deposito.query.get(deposito_id)
    
    @staticmethod
    def calcular_total_depositos(cuenta_id):
        """
        Calcula el total de depósitos de una cuenta
        """
        from sqlalchemy import func
        
        total = db.session.query(func.sum(Deposito.monto))\
            .filter(Deposito.id_cuenta == cuenta_id)\
            .filter(Deposito.estado == 'completado')\
            .scalar() or 0
            
        return float(total)