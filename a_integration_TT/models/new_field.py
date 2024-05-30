from odoo import models, fields, api, _


class PosOrderNew(models.Model):
    _inherit = "pos.order.line"

    receipt_uniq = fields.Char(
        required=True, copy=False, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, vals):
        print("Pos Ref", vals)
        vals["receipt_uniq"] = self.env["ir.sequence"].next_by_code("pos.seq")
        return super(PosOrderNew, self).create(vals)


class PosOrderNext(models.Model):
    _inherit = "pos.order"

    receipt_uniq_2 = fields.Char(
        required=True, copy=False, readonly=True, default=lambda self: _("New")
    )

    @api.model
    def create(self, vals):
        print("Pos Ref", vals)
        vals["receipt_uniq_2"] = self.env["ir.sequence"].next_by_code("pos.seq.tem")
        return super(PosOrderNext, self).create(vals)

    def export_for_printing(self):
        # Prepare data for printing
        data = {
            "receipt_uniq_2": self.receipt_uniq_2,
        }
        return data
