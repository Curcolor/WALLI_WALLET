from .viewpages_route import bp as viewpages_bp
from .auth import bp as auth_bp
from .deposito_route import bp as deposito_bp
from .retiro_route import bp as retiro_bp
from .servicio_route import bp as servicio_bp
from .pago_servicio__route import bp as pago_servicio_bp
from .cuenta_route import bp as cuenta_bp
from .transferencia_route import bp as transferencia_bp
from .walli_route import bp as walli_bp

blueprints = [
    viewpages_bp,
    auth_bp,
    deposito_bp,
    retiro_bp,
    servicio_bp,
    pago_servicio_bp,
    cuenta_bp,
    transferencia_bp,
    walli_bp
] 