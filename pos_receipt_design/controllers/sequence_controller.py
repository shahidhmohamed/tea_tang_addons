from odoo import http
from odoo.http import request, Response

class SequenceController(http.Controller):

    @http.route('/api/sequence/<string:shop_name>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_sequence_number(self, shop_name, **kwargs):
        try:
            # Get the current sequence number for the shop
            sequence_number = request.env['ir.config_parameter'].sudo().get_param('sequence_number_' + shop_name)
            sequence_number = int(sequence_number) if sequence_number else 1

            # Increment the sequence number
            sequence_number += 1

            # Update the sequence number in the configuration parameters
            request.env['ir.config_parameter'].sudo().set_param('sequence_number_' + shop_name, sequence_number)

            return Response('Sequence number updated successfully', status=200)

        except Exception as e:
            return Response('Error updating sequence number: ' + str(e), status=500)
