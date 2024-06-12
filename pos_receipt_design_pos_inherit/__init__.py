from . import models

def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import UserError, ValidationError
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '17.0':
        raise UserError(f'Module support Odoo series 17.0 but found {server_serie}.')
    return True
