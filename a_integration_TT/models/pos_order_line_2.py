from odoo import models, fields, api, _


class TeaOrderLineTow(models.Model):
    _name = "tea.order.line.2"
    _order = "session_id desc"

    tea_tang_line_conn_2 = fields.Many2one("tea.order.new")
    session_id = fields.Integer(string="ID")
    ReceiptDate = fields.Date(string="Receipt Date")
    cardtype = fields.Char(string="Card Type")
    paymentDate = fields.Date(string="Payment Date")
    ReceiptNo = fields.Char(string="Receipt No")
    PaymentAmt = fields.Float(string="Payment Amount")
    PaymentMethods = fields.Char(string="Payment method")
    company = fields.Char(string="Company")
    SalesType = fields.Char(string="Sales Type")


class PosPayment(models.Model):
    _inherit = "pos.payment"

    @api.model
    def create(self, vals):
        record = super(PosPayment, self).create(vals)
        record._update_tea_order_line_2()
        return record

    def _update_tea_order_line_2(self):
        tea_order_line_2 = self.env["tea.order.line.2"]

        # Fetch the corresponding pos.order record using the pos_order_id from pos.payment
        order = self.env["pos.order"].browse(self.pos_order_id.id)

        # company list
        allowed_companies = [
            # "Tea Tang Group",
            # "Tea Tang (Pvt) Ltd",
            # "Tea Tang - Liberty Plaza",
            "Tea Tang - One Galle Face Mall",
            # "Tea Tang - Shakti Gallery",
            # "SHA Foundation",
            "SHA Foundation - One Galle Face Mall",
            # "SHA Foundation - Shakti Gallery",
        ]

        # Check if the company name is in the allowed list
        if self.company_id.name in allowed_companies:

            # Create record in tea.order.line.2
            tea_order_line_2.create(
                {
                    "PaymentAmt": self.amount,
                    "ReceiptNo": order.pos_reference,
                    "company": self.company_id.name,
                    "ReceiptDate": self.create_date,
                    "session_id": self.pos_order_id.id,
                    "cardtype": self.card_type,
                    "PaymentMethods": self.payment_method_id.name,
                    "SalesType": self.name,
                }
            )
