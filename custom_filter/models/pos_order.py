from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    current_company = fields.Char(string='Current Company', compute='_compute_current_company')

    def _compute_current_company(self):
        for record in self:
            record.current_company = self.env.company.name
    
    cat_company = fields.Char(
        string='Company From Category',
        related='categ_id.company',
        store=True
    )

    def userr(self):
        for record in self:
            if record.current_company == record.cat_company:
                raise UserError("Hello im shahidh," 
                                                                                                                                                                                                                                                                                                                                                                                                      
                                "kakka dammada mr.Tharanga")
            else:
                raise UserError("Kakka baraida")


class ProductCategory(models.Model):
    _inherit = 'product.category'

    company = fields.Char(string='Company',store=True)
