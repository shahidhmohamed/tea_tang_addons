from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    partner_ref = fields.Char(string="Partner Ref", related='order_id.partner_ref', store=True)



class Picking(models.Model):
    _inherit = "stock.picking"

    # This code is working But There is a issu to check that is that working or is that changing the price unit as for product and confirm the
    def button_update_valuation_layer_value(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                if move.id:
                    # Search for the stock valuation layer with matching stock move ID
                    valuation_layer = self.env['stock.valuation.layer'].search([('stock_move_id', '=', move.id)], limit=1)
                    
                    # Search for all purchase order lines with matching partner reference
                    purchase_order_lines = self.env['purchase.order.line'].search([('partner_ref', '=', move.reference_ne_ms)])
                    
                    # Update the valuation_layer_value field in stock move
                    if valuation_layer:
                        move.valuation_layer_value = abs(valuation_layer.value)
                    
                    # Iterate over each purchase order line and update the price unit
                    for purchase_order_line in purchase_order_lines:
                        # Update the from_po field in stock move if it matches
                        if purchase_order_line:
                            move.form_po = purchase_order_line.order_id.id

                            # Check if the purchase order line has an order_id and matches the stock move's form_po
                            if purchase_order_line.order_id.id == move.form_po and purchase_order_line.product_id == move.product_id:
                                # Update the price_unit in purchase order line using stock move's cost_per_unit
                                purchase_order_line.price_unit = move.cost_per_unit



class StockMove(models.Model):
    _inherit = "stock.move"

    valuation_layer_value = fields.Float("Total Cost")
    cost_per_unit = fields.Float("Cost Per Unit", compute='_compute_cost_per_unit', store=True)
    reference_ne_ms = fields.Char(string="Partner Ref", related='picking_id.origin', store=True)
    form_po = fields.Integer(string="Order ID", store=True)

    @api.depends('valuation_layer_value', 'quantity')
    def _compute_cost_per_unit(self):
        for record in self:
            if record.valuation_layer_value and record.quantity:
                record.cost_per_unit = record.valuation_layer_value / record.quantity
            else:
                record.cost_per_unit = 0.0






