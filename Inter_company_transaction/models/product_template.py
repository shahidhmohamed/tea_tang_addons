from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from pytz import UTC

from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, get_lang
from odoo.tools.float_utils import float_compare, float_round
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    new_cost = fields.Float("New Cost")

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # @api.depends('product_qty', 'product_uom', 'company_id')
    # def _compute_price_unit_and_date_planned_and_name(self):
    #     for line in self:
    #         if not line.product_id or line.invoice_lines or not line.company_id:
    #             continue

    #         # Directly use new_cost from the product template
    #         po_line_uom = line.product_uom or line.product_id.uom_po_id
    #         price_unit = line.env['account.tax']._fix_tax_included_price_company(
    #             line.product_id.uom_id._compute_price(line.product_id.product_tmpl_id.new_cost, po_line_uom),
    #             line.product_id.supplier_taxes_id,
    #             line.taxes_id,
    #             line.company_id,
    #         )
    #         price_unit = line.product_id.cost_currency_id._convert(
    #             price_unit,
    #             line.currency_id,
    #             line.company_id,
    #             line.date_order or fields.Date.context_today(line),
    #             False
    #         )
    #         line.price_unit = float_round(price_unit, precision_digits=max(line.currency_id.decimal_places, self.env['decimal.precision'].precision_get('Product Price')))

    #         params = {'order_id': line.order_id}
    #         seller = line.product_id._select_seller(
    #             partner_id=line.partner_id,
    #             quantity=line.product_qty,
    #             date=line.order_id.date_order and line.order_id.date_order.date() or fields.Date.context_today(line),
    #             uom_id=line.product_uom,
    #             params=params)

    #         if seller or not line.date_planned:
    #             line.date_planned = line._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    #         # Record product names to avoid resetting custom descriptions
    #         default_names = []
    #         vendors = line.product_id._prepare_sellers({})
    #         for vendor in vendors:
    #             product_ctx = {'seller_id': vendor.id, 'lang': get_lang(line.env, line.partner_id.lang).code}
    #             default_names.append(line._get_product_purchase_description(line.product_id.with_context(product_ctx)))
    #         if not line.name or line.name in default_names:
    #             product_ctx = {'seller_id': seller.id, 'lang': get_lang(line.env, line.partner_id.lang).code}
    #             line.name = line._get_product_purchase_description(line.product_id.with_context(product_ctx))

    new_cost = fields.Float("New Cost", compute='_get_new_cost', store=True)

    @api.depends('product_id')
    def _get_new_cost(self):
        for record in self:
            if record.product_id:
                record.new_cost = record.product_id.product_tmpl_id.new_cost
            else:
                record.new_cost = 0.0