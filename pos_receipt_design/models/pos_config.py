from odoo import fields, models, _

class PosConfig(models.Model):
    _inherit = 'pos.config'

    use_custom_receipt = fields.Boolean(string="Use Custom Receipt")
    receipt_design_id = fields.Many2one('receipt.design', string="Receipt Design")

    sale_receipt = fields.Boolean(string='sale receipt')
    sale_receipt_sequence_ids = fields.Many2one(
        'ir.sequence', string="Set receipt sequence number")
    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    use_custom_receipt = fields.Boolean(string="Use Custom Receipt", related='pos_config_id.use_custom_receipt', readonly=False)
    receipt_design_id = fields.Many2one('receipt.design', string="Receipt Design", related='pos_config_id.receipt_design_id', readonly=False)