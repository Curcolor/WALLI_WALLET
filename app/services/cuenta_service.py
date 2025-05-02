from app.models import Cuenta, Cliente, Deposito, Retiro, Transaccion, PagoServicio, Servicio
from app.extensions import db
from sqlalchemy.sql import func
import random

class CuentaService:
    @staticmethod
    def get_info_cuenta(cuenta_id):
        """Obtiene la información principal de la cuenta"""
        cuenta = Cuenta.query.join(Cliente).filter(Cuenta.id_cuenta == cuenta_id).first()
        
        if not cuenta:
            return None
            
        return {
            'nombre_usuario': f"{cuenta.cliente.nombre} {cuenta.cliente.apellido}",
            'saldo_actual': float(cuenta.saldo_actual)
        }
    
    @staticmethod
    def obtener_saldo(cuenta_id):
        """Obtiene el saldo actual de una cuenta"""
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
        return float(cuenta.saldo_actual)
    
    @staticmethod
    def realizar_deposito(cuenta_id, monto, canal='web'):
        """Realiza un depósito en la cuenta"""
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
            
        if cuenta.estado != 'activa':
            raise ValueError("La cuenta no está activa")
            
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
            
        # Crear el registro de depósito
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
        
        return {
            'id_deposito': deposito.id_deposito,
            'nuevo_saldo': float(cuenta.saldo_actual)
        }
    
    @staticmethod
    def realizar_retiro(cuenta_id, monto, canal='web'):
        """Realiza un retiro de la cuenta"""
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
            
        if cuenta.estado != 'activa':
            raise ValueError("La cuenta no está activa")
            
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
            
        if float(cuenta.saldo_actual) < monto:
            raise ValueError("Saldo insuficiente")
            
        # Generar código de retiro
        codigo_retiro = ''.join(random.choices('0123456789', k=6))
        
        # Crear el registro de retiro
        retiro = Retiro(
            id_cuenta=cuenta_id,
            monto=monto,
            canal_retiro=canal,
            codigo_retiro=codigo_retiro,
            estado='completado'
        )
        
        # Actualizar saldo
        cuenta.saldo_actual = float(cuenta.saldo_actual) - float(monto)
        
        db.session.add(retiro)
        db.session.commit()
        
        return {
            'id_retiro': retiro.id_retiro,
            'codigo_retiro': codigo_retiro,
            'nuevo_saldo': float(cuenta.saldo_actual)
        }
    
    @staticmethod
    def realizar_transferencia(cuenta_origen_id, numero_telefono_destino, monto, descripcion=None, canal='web'):
        """Realiza una transferencia entre cuentas"""
        cuenta_origen = Cuenta.query.get(cuenta_origen_id)
        if not cuenta_origen:
            raise ValueError("Cuenta origen no encontrada")
            
        if cuenta_origen.estado != 'activa':
            raise ValueError("La cuenta origen no está activa")
            
        if float(cuenta_origen.saldo_actual) < monto:
            raise ValueError("Saldo insuficiente")
            
        cuenta_destino = Cuenta.query.filter_by(numero_telefono_ingreso=numero_telefono_destino).first()
        if not cuenta_destino:
            raise ValueError("Cuenta destino no encontrada")
            
        if cuenta_destino.id_cuenta == cuenta_origen_id:
            raise ValueError("No puede transferir a su propia cuenta")
            
        if cuenta_destino.estado != 'activa':
            raise ValueError("La cuenta destino no está activa")
            
        # Crear la transacción
        transaccion = Transaccion(
            id_cuenta_origen=cuenta_origen_id,
            id_cuenta_envio=cuenta_destino.id_cuenta,
            monto=monto,
            descripcion=descripcion,
            canal=canal,
            estado='completado'
        )
        
        # Actualizar saldos
        cuenta_origen.saldo_actual = float(cuenta_origen.saldo_actual) - float(monto)
        cuenta_destino.saldo_actual = float(cuenta_destino.saldo_actual) + float(monto)
        
        db.session.add(transaccion)
        db.session.commit()
        
        return {
            'id_transaccion': transaccion.id_transaccion,
            'nuevo_saldo': float(cuenta_origen.saldo_actual)
        }
        
    @staticmethod
    def pagar_servicio(cuenta_id, servicio_id, monto, referencia=None):
        """Realiza el pago de un servicio"""
        from app.models import Servicio
        
        cuenta = Cuenta.query.get(cuenta_id)
        if not cuenta:
            raise ValueError("Cuenta no encontrada")
            
        if cuenta.estado != 'activa':
            raise ValueError("La cuenta no está activa")
            
        if float(cuenta.saldo_actual) < monto:
            raise ValueError("Saldo insuficiente")
            
        servicio = Servicio.query.get(servicio_id)
        if not servicio:
            raise ValueError("Servicio no encontrado")
            
        if servicio.estado != 'activo':
            raise ValueError("El servicio no está disponible")
            
        # Crear el pago
        pago = PagoServicio(
            id_cuenta=cuenta_id,
            id_servicio=servicio_id,
            monto=monto,
            referencia=referencia,
            estado='completado'
        )
        
        # Actualizar saldo
        cuenta.saldo_actual = float(cuenta.saldo_actual) - float(monto)
        
        db.session.add(pago)
        db.session.commit()
        
        return {
            'id_pago': pago.id_pago,
            'nuevo_saldo': float(cuenta.saldo_actual)
        }
    
    @staticmethod
    def obtener_transacciones_recientes(cuenta_id, limit=10):
        """Obtiene las transacciones recientes de una cuenta"""
        from sqlalchemy import union_all, desc
        from app.models import Deposito, Retiro, Transaccion, PagoServicio
        
        # Consulta para depósitos
        depositos_query = db.session.query(
            func.cast('DEPOSITO', db.String).label('tipo_transaccion'),
            Deposito.monto.label('monto'),
            Deposito.fecha_deposito.label('fecha_transaccion'),
            func.cast('Depósito realizado', db.String).label('descripcion'),
            Deposito.estado.label('estado')
        ).filter(Deposito.id_cuenta == cuenta_id)
        
        # Consulta para retiros
        retiros_query = db.session.query(
            func.cast('RETIRO', db.String).label('tipo_transaccion'),
            Retiro.monto.label('monto'),
            Retiro.fecha_retiro.label('fecha_transaccion'),
            func.cast('Retiro de dinero', db.String).label('descripcion'),
            Retiro.estado.label('estado')
        ).filter(Retiro.id_cuenta == cuenta_id)
        
        # Consulta para transferencias enviadas
        transferencias_enviadas_query = db.session.query(
            func.cast('TRANSFERENCIA', db.String).label('tipo_transaccion'),
            Transaccion.monto.label('monto'),
            Transaccion.fecha_transaccion.label('fecha_transaccion'),
            func.cast('Transferencia enviada', db.String).label('descripcion'),
            Transaccion.estado.label('estado')
        ).filter(Transaccion.id_cuenta_origen == cuenta_id)
        
        # Consulta para transferencias recibidas
        transferencias_recibidas_query = db.session.query(
            func.cast('TRANSFERENCIA', db.String).label('tipo_transaccion'),
            Transaccion.monto.label('monto'),
            Transaccion.fecha_transaccion.label('fecha_transaccion'),
            func.cast('Transferencia recibida', db.String).label('descripcion'),
            Transaccion.estado.label('estado')
        ).filter(Transaccion.id_cuenta_envio == cuenta_id)
        
        # Consulta para pagos de servicios
        pagos_servicios_query = db.session.query(
            func.cast('SERVICIO', db.String).label('tipo_transaccion'),
            PagoServicio.monto.label('monto'),
            PagoServicio.fecha_pago.label('fecha_transaccion'),
            func.concat('Pago de ', db.func.coalesce(Servicio.nombre_servicio, 'servicio')).label('descripcion'),
            PagoServicio.estado.label('estado')
        ).join(
            Servicio, PagoServicio.id_servicio == Servicio.id_servicio, isouter=True
        ).filter(PagoServicio.id_cuenta == cuenta_id)
        
        # Combinar todas las consultas
        combined_query = union_all(
            depositos_query, 
            retiros_query, 
            transferencias_enviadas_query,
            transferencias_recibidas_query,
            pagos_servicios_query
        ).order_by(desc('fecha_transaccion')).limit(limit)
        
        return db.session.execute(combined_query).fetchall()