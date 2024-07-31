from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    no_negative_stock = fields.Boolean(
        string="No negative stock",
        readonly=False,
        help="Allows you to prohibit negative stock quantities.",
    )

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('res.config.settings.no_negative_stock', self.no_negative_stock)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            no_negative_stock=self.env['ir.config_parameter'].sudo().get_param('res.config.settings.no_negative_stock', default=False),
        )
        return res
