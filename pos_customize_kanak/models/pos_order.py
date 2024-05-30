# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    pos_customer_code = fields.Char(string='Order Number')

    def _get_fields_for_draft_order(self):
        fields = super(PosOrder, self)._get_fields_for_draft_order()
        fields.extend([
            'pos_customer_code',
        ])
        return fields

    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['pos_customer_code'] = ui_order.get('pos_customer_code')
        return res

    def _export_for_ui(self, order):
        result = super(PosOrder, self)._export_for_ui(order)
        result['pos_customer_code'] = order.pos_customer_code
        return result
