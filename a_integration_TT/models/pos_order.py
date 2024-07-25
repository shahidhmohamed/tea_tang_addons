from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TeaOrder(models.Model):
    _name = "tea.order.new"

    custom_name = fields.Char(string="Custom Name")
    pos_connect = fields.One2many("tea.order.line", "tea_tang_line_conn")
    pos_connect_lien_2 = fields.One2many("tea.order.line.2", "tea_tang_line_conn_2")
    session_id = fields.Integer(string="id")
