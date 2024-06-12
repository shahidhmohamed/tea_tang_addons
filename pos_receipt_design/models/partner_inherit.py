from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    # Adding a new field related to the 'name' field in 'pos.order'
    new = fields.Char(string='New Field', related="send.name")

    # Adding a Many2one field linking to 'pos.order'
    send = fields.Many2one('pos.order', string="PURCHASE ORDER NUMBER")

    # Overriding the method to load additional models in the POS UI
    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result.append('pos.order')
        return result
    
    # Defining loader parameters for a custom model
    def _loader_params_pos_order(self):
        return {      
            'search_params': {          
                # 'domain': [('state', '=', 'draft')],  # Example domain filter
                'fields': [
                    'name','pos_reference'],          
            },  
        }

    # Method to get the data for the POS UI for a custom model
    def _get_pos_ui_pos_order(self, params):
        return self.env['pos.order'].search_read(**params['search_params'])
