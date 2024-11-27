from .cliente import Cliente
from .cuenta import Cuenta
from .deposito import Deposito
from .retiro import Retiro
from .servicio import Servicio
from .pago_servicio import PagoServicio
from .transaccion import Transaccion

models = [
    Cliente,
    Cuenta,
    Deposito,
    Retiro,
    Servicio,
    PagoServicio,
    Transaccion
] 