from app.extensions import login_manager
from app.models.cliente import Cliente
from app.models.cuenta import Cuenta
from app.models.deposito import Deposito
from app.models.retiro import Retiro
from app.models.transaccion import Transaccion
from app.models.servicio import Servicio
from app.models.pago_servicio import PagoServicio

@login_manager.user_loader
def load_user(user_id):
    return Cuenta.query.get(int(user_id))

__all__ = ['Cliente', 'Cuenta', 'Deposito', 'Retiro', 
           'Transaccion', 'Servicio', 'PagoServicio']