from odoo import models, fields, api, _


class TeaOrderLineTow(models.Model):
    _name = "tea.order.line.2"

    tea_tang_line_conn_2 = fields.Many2one("tea.order.new")
    session_id = fields.Integer(string="ID")
    ReceiptDate = fields.Date(string="RECEIPT DATE")
    cardtype = fields.Char(string="CARD TYPE")
    paymentDate = fields.Date(string="PAYMENT DATE")
    ReceiptNo = fields.Char(string="RECEIPT NO")
    PaymentAmt = fields.Float(string="PAYMENT AMT")
    PaymentMethods = fields.Char(string="PAYMENT METHOD")
    company = fields.Char(string="COMPANY")
    SalesType = fields.Char(string="SALES TYPE")
