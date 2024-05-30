# from odoo import models, fields, api, _

# class PosOrder(models.Model):
#     _inherit = 'pos.order'

#     def write(self, vals):
#         # Call the superclass method to execute the original write logic of pos.order
#         result = super(PosOrder, self).write(vals)

#         # Check if 'session_id' is provided in vals
#         if 'session_id' in vals:
#             # Retrieve the session_id from vals
#             session_id = vals['session_id']

#             # Loop through each updated pos.order record
#             for pos_order in self:
#                 # Create a corresponding record in tea.order for each updated pos.order
#                 tea_order_obj = self.env['tea.order.new']
#                 tea_order_vals = {
#                     # Map the fields from pos_order to tea_order
#                     'custom_name': pos_order.name,
#                     'session_id': session_id,
#                     # Add other fields as needed
#                 }
#                 tea_order = tea_order_obj.create(tea_order_vals)

#         return result



