from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    

    # def button_mark_done_test(self):
    #     for production in self:
    #         # Iterate over the moves related to this production
    #         for move in production.move_raw_ids:
    #             # Ensure 'quantity' and 'on_hand_qty' are available from the stock.move model
    #             if move.quantity > move.on_hand_qty:
    #                 raise ValidationError("You cannot produce more than the available quantity of the product.")
                
    def button_mark_done(self):
        # Fetch the 'no_negative_stock' setting from ir.config_parameter
        config_param = self.env['ir.config_parameter'].sudo()
        no_negative_stock = config_param.get_param('res.config.settings.no_negative_stock', default='False')
        no_negative_stock = no_negative_stock == 'True'
        
        if no_negative_stock:
            for production in self:
                # Iterate over the moves related to this production
                for move in production.move_raw_ids:
                    quantity = move.quantity
                    on_hand_qty = move.on_hand_qty

                    # Handle cases where quantity or on_hand_qty could be empty strings
                    if isinstance(quantity, str) and quantity.strip() == '':
                        quantity = 0.0
                    if isinstance(on_hand_qty, str) and on_hand_qty.strip() == '':
                        on_hand_qty = 0.0

                    # Raise error if quantity and on_hand_qty are both zero or if quantity is greater than on_hand_qty
                    if (quantity == 0.0 and on_hand_qty == 0.0) or quantity > on_hand_qty:
                        raise ValidationError("You cannot produce more than the available quantity of the product.")
        
        return super(MrpProduction, self).button_mark_done()
                

class StockMove(models.Model):
    _inherit = 'stock.move'

    on_hand_qty = fields.Float(
        string='On Hand QTY',
        related='product_id.qty_available',
        readonly=True,
        store=True
    )

    