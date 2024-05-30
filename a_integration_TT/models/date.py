from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Date(models.Model):
    _name = "date"

    date = fields.Datetime(string="DATE")
    tea_connect = fields.One2many(
        "tea.order.line", "date_connect", string="tea connect"
    )
