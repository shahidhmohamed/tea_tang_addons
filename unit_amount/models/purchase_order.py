from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # unit_amount = fields.Float (string='Unit Amount')
    
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    unit_amount = fields.Float (string='Unit Amount')


    @api.onchange('unit_amount')
    def replace_unit_price(self):
        for record in self:
            # Check if price_unit is empty (assuming 0.0 is considered empty)
            if record.unit_amount and record.price_unit == 0.0:
                record.price_unit = record.unit_amount