from odoo import models, fields, api, _
from lxml import etree

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    unit_amount = fields.Integer(string='Unit Amount')

    # vendor_group = fields.Selection(
    #     related='order_id.Vendor_group',
    #     string='Vendor Group',
    #     readonly=True,
    #     store=True
    # )

    new_total_amount_taxed = fields.Monetary(string='Line Amount', compute='_compute_new_total_amount')
    line_amount_tax_excl = fields.Monetary(string='Line Amount Excl', compute='_compute_new_total_amount')

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_new_total_amount(self):
        for line in self:
            new_total_amount = line.unit_amount * line.product_qty
            if new_total_amount > 0:
                taxes = line.taxes_id.compute_all(new_total_amount, line.order_id.currency_id, 1, product=line.product_id, partner=line.order_id.partner_id)
                line.new_total_amount_taxed = taxes['total_included']
                line.line_amount_tax_excl = taxes['total_excluded']
            else:
                line.new_total_amount_taxed = 0.00
                line.line_amount_tax_excl = 0.00

    @api.onchange('unit_amount', 'product_qty')
    def _onchange_unit_amount_or_product_qty(self):
        for record in self:
            if record.unit_amount:
                record.price_unit = record.unit_amount

    def write(self, vals):
        res = super(PurchaseOrderLine, self).write(vals)
        if 'unit_amount' in vals or 'product_qty' in vals:
            self._onchange_unit_amount_or_product_qty()
        return res

    @api.model
    def create(self, vals):
        record = super(PurchaseOrderLine, self).create(vals)
        if 'unit_amount' in vals or 'product_qty' in vals:
            record._onchange_unit_amount_or_product_qty()
        return record


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    tax_totals_new = fields.Monetary(compute='_compute_tax_totals_new', string='Total Line Amount Including Tax', store=True)
    # Vendor_group = fields.Selection(
    #     string='Vendor Group',
    #     # related='partner_id.x_studio_vendor_group',
    #     readonly=True,
    #     store=True
    # )

    @api.depends('order_line.new_total_amount_taxed')
    def _compute_tax_totals_new(self):
        for order in self:
            order.tax_totals_new = sum(order.order_line.mapped('new_total_amount_taxed'))

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            for line in order.order_line:
                if line.unit_amount:
                    line.price_unit = line.unit_amount
        return res
