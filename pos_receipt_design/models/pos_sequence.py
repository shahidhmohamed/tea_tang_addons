from odoo import api, fields, models, _

class PosSeq(models.Model):
    _name = "pos.sequence"
    _rec_name = "shop_name"

    shop_name = fields.Char(string="shop_name")