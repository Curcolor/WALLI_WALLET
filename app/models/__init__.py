from .cliente import Cliente
from .cuenta import Cuenta
from .deposito import deposito
from .retiro import Retiro
from .servicio import Servicio
from .pago_servicio import PagoServicio
from .transaccion import transaccion

models = [
    Cliente,
    Cuenta,
    deposito,
    Retiro,
    Servicio,
    PagoServicio,
    transaccion
] 