from odoo import api, fields, models

class ResPartner(models.Model):
   _inherit = "res.partner"

   vendor_group = fields.Selection(string='vendor group',
        selection=[('internal', 'Internal'), ('external', 'External')],
        compute='_compute_vendor_group', inverse='_write_vendor_group')
   
   @api.depends('vendor_group')
   def _compute_vendor_group(self):
      for partner in self:
         if partner.vendor_group == 'internal':
            partner.vendor_group = 'Internal'
         else:
            partner.vendor_group = False

   @api.depends('vendor_group')
   def _write_vendor_group(self):
      for partner in self:
         if partner.vendor_group == 'external':
            partner.vendor_group = 'External'
         else:
            partner.vendor_group = False
