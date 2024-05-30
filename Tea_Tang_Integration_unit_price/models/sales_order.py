from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    new_field = fields.Integer(string="my field" , store=True)
    name_lbx = fields.Char(string="Name Lbx" , related='order_id.name', store=True)
    partner_ref = fields.Char(string="Partner Ref" , related='order_id.partner_ref', store=True)


class SaleOrder(models.Model):
    _inherit = "sale.order"



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    def unit_confirm(self):
        purchase_order_lines = self.env['purchase.order.line'].search([])
        sale_order_lines = self.env['sale.order.line'].search([])

        for purchase_order_line in purchase_order_lines:
            sale_order_lines_matched = sale_order_lines.filtered(lambda l: l.client_order_ref == purchase_order_line.name_lbx and l.product_id.id == purchase_order_line.product_id.id and l.name_lbx == purchase_order_line.partner_ref)
            for sale_order_line_matched in sale_order_lines_matched:
                purchase_order_line.write({'price_unit': sale_order_line_matched.price_unit})


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"



    client_order_ref = fields.Char(string="Client Order Ref" , related='order_id.client_order_ref', store=True)
    name_lbx = fields.Char(string="Name Lbx" , related='order_id.name', store=True)
