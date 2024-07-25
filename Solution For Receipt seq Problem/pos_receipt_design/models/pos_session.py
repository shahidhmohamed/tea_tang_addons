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
                    'name'],          
            },  
        }

    # Method to get the data for the POS UI for a custom model
    def _get_pos_ui_pos_order(self, params):
        return self.env['pos.order'].search_read(**params['search_params'])
    
    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        if self.config_id.sale_receipt and self.config_id.sale_receipt_sequence_ids:
            result.append('ir.sequence')
            result.append('ir.sequence.date_range')
        return result

    def _loader_params_ir_sequence(self):
        data = {
            'search_params': {
                'domain': [('id', '=', self.config_id.sale_receipt_sequence_ids[0].id)],
            }
        }
        return data

    def _loader_params_ir_sequence_date_range(self):
        data2 =  {'search_params': {'domain': [], 'fields': ['date_from', 'date_to', 'number_next_actual']}}
        return data2

    def _get_pos_ui_ir_sequence(self, params):
        return self.env['ir.sequence'].search_read(**params['search_params'])

    def _get_pos_ui_ir_sequence_date_range(self, params):
        return self.env['ir.sequence.date_range'].search_read(**params['search_params'])
