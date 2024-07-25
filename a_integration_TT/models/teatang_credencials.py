from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class Credentials(models.Model):
    _name = "tea.credentials"
    # _description = "Credentials"

    customer_id = fields.Char(string="Client ID")
    secret_client = fields.Char(string="Client Code")
    token_url = fields.Char(string="Token URL")
    ogf_url = fields.Char(string="OGF WebService")
    app_code = fields.Char(string="App Code")
    property_code = fields.Char(string="Property Code")
    #
    # _sql_constraints = [
    #     ("unique_credentials", "unique(id)", "Only one set of credentials is allowed.")
    # ]

    # @api.model
    # def create(self, vals):
    #     if self.search_count([]) >= 1:
    #         raise UserError(
    #             _(
    #                 "You can only create one set of credentials. Please modify the existing one."
    #             )
    #         )
    #     return super(Credentials, self).create(vals)

    # def unlink(self):
    #     raise UserError(
    #         _(
    #             "You cannot delete the credentials. Please modify the existing one if needed."
    #         )
    #     )

    # @api.model
    # def default_get(self, fields):
    #     res = super(Credentials, self).default_get(fields)
    #     if self.search_count([]) >= 1:
    #         record = self.search([], limit=1)
    #         if record:
    #             res.update(
    #                 {
    #                     "customer_id": record.customer_id,
    #                     "secret_client": record.secret_client,
    #                     "token_url": record.token_url,
    #                     "ogf_url": record.ogf_url,
    #                     "app_code": record.app_code,
    #                     "property_code": record.property_code,
    #                 }
    #             )
    #     return res
