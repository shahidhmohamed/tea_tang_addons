from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    
    


    # def print_receipt(self):
    #     raise UserError("Printing")

    def print_receipt(self):
        # Here you can add any specific logic before printing the receipt
        return self.env.ref('reprint_download.action_pos_receipt_re_print').report_action(self, config=True)



# class PosOrder(models.Model):
#     _inherit = "pos.payment"


#     pay_ref = fields.Char(string="Pay Ref")