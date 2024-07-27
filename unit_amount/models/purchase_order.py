from odoo import models, fields, api, _
from lxml import etree

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    unit_amount = fields.Integer(string='Unit Amount')
    override_price_unit = fields.Boolean(string='Override Price Unit', default=True)

    new_total_amount_taxed = fields.Monetary(string='Line Amount', compute='_compute_new_total_amount')
    line_amount_tax_excl = fields.Monetary(string='Line Amount Excl', compute='_compute_new_total_amount')
    vendor_group = fields.Selection(
        related='order_id.Vendor_group',
        string='Vendor Group',
        readonly=True,
        store=True
    )

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
            if record.unit_amount or record.unit_amount == 0:
                record.price_unit = record.unit_amount

    def write(self, vals):
        if 'unit_amount' in vals or 'product_qty' in vals:
            for record in self:
                if 'unit_amount' in vals:
                    if vals['unit_amount'] == 0:
                        vals['price_unit'] = 0
                    elif record.override_price_unit:
                        vals['price_unit'] = vals.get('unit_amount', record.unit_amount)
        res = super(PurchaseOrderLine, self).write(vals)
        return res


    @api.model
    def create(self, vals):
        if 'unit_amount' in vals:
            if vals['unit_amount'] == 0:
                vals['price_unit'] = 0
            elif vals.get('override_price_unit', True):
                vals['price_unit'] = vals.get('unit_amount', 0)
        record = super(PurchaseOrderLine, self).create(vals)
        return record


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Please note this if internal server appears please comment this realated parameter "related='partner_id.x_studio_vendor_group'b"
    tax_totals_new = fields.Monetary(compute='_compute_tax_totals_new', string='Total Line Amount Including Tax', store=True)
    Vendor_group = fields.Selection(
        string='Vendor Group',
        related='partner_id.x_studio_vendor_group',
        readonly=True,
        store=True
    )

    @api.depends('order_line.new_total_amount_taxed')
    def _compute_tax_totals_new(self):
        for order in self:
            order.tax_totals_new = sum(order.order_line.mapped('new_total_amount_taxed'))

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            for line in order.order_line:
                if line.unit_amount == 0:
                    line.price_unit = 0
                elif line.override_price_unit:
                    line.price_unit = line.unit_amount
        return res
