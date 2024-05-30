from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Picking(models.Model):
    _inherit = "stock.picking"

    def button_update_valuation_layer_value(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                if move.id:
                    valuation_layer = self.env['stock.valuation.layer'].search([('stock_move_id', '=', move.id)], limit=1)
                    if valuation_layer:
                        move.valuation_layer_value = abs(valuation_layer.value)


class StockMove(models.Model):
    _inherit = "stock.move"

    valuation_layer_value = fields.Float("Total Cost")
    cost_per_unit = fields.Float("Cost Per Unit", compute='_compute_cost_per_unit', store=True)

    @api.depends('valuation_layer_value', 'quantity')
    def _compute_cost_per_unit(self):
        for record in self:
            if record.valuation_layer_value and record.quantity:
                record.cost_per_unit = record.valuation_layer_value / record.quantity
            else:
                record.cost_per_unit = 0.0


class StockValuationLayer(models.Model):
    """Stock Valuation Layer"""

    _inherit = 'stock.valuation.layer'

    unit_cost = fields.Float('Unit Value', digits='Product Price', readonly=True, group_operator=None, compute='_get_unit_cost')


    @api.depends('product_id')
    def _get_unit_cost(self):
        for record in self:
            if record.product_id:
                record.unit_cost = record.product_id.product_tmpl_id.new_cost
            else:
                record.unit_cost = 0.0