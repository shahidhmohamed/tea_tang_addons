# from odoo import models, fields, api, _
# from odoo.exceptions import UserError


# class Date(models.Model):
#     _name = "date"

#     date = fields.Datetime(string="Start Date", required=True)
#     e_date = fields.Datetime(string="End Date", required=True)
#     tea_connect = fields.One2many(
#         "tea.order.line", "date_connect", string="tea connect"
#     )

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Date(models.Model):
    _name = "date"
    _description = "Settings"
    _rec_name = "settings"

    date = fields.Datetime(string="Start Date", required=True)
    e_date = fields.Datetime(string="End Date", required=True)
    tea_connect = fields.One2many(
        "tea.order.line", "date_connect", string="Tea Connect"
    )
    customer_id = fields.Char(string="Client ID")
    secret_client = fields.Char(string="Client Code")
    token_url = fields.Char(string="Token URL")
    ogf_url = fields.Char(string="OGF WebService")
    app_code = fields.Char(string="App Code")
    property_code = fields.Char(string="Property Code")
    settings = fields.Char(string="Settings", default="Settings")

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
    #     return super(Date, self).create(vals)

    # def unlink(self):
    #     raise UserError(
    #         _(
    #             "You cannot delete the credentials. Please modify the existing one if needed."
    #         )
    #     )

    # @api.model
    # def default_get(self, fields):
    #     res = super(Date, self).default_get(fields)
    #     if self.search_count([]) >= 1:
    #         record = self.search([], limit=1)
    #         if record:
    #             res.update(
    #                 {
    #                     "date": record.date,
    #                     "e_date": record.e_date,
    #                     "customer_id": record.customer_id,
    #                     "secret_client": record.secret_client,
    #                     "token_url": record.token_url,
    #                     "ogf_url": record.ogf_url,
    #                     "app_code": record.app_code,
    #                     "property_code": record.property_code,
    #                 }
    #             )
    #     return res

    # @api.model
    # def create(self, vals):
    #     # Prevent creating new records
    #     if self.env["date"].search([]):
    #         raise UserError(_("Cannot create new records. Only one record is allowed."))
    #     return super(Date, self).create(vals)

    # def write(self, vals):
    #     # Ensure only updating the record with ID 1
    #     if self.id != 1:
    #         raise UserError(
    #             _(
    #                 "Cannot update this record. Only the record with ID 1 can be updated."
    #             )
    #         )
    #     return super(Date, self).write(vals)

    # @api.model
    # def default_get(self, fields):
    #     res = super(Date, self).default_get(fields)
    #     # Load the default values from record ID 1
    #     default_rec = self.browse(1)
    #     if default_rec:
    #         res.update(
    #             {
    #                 "date": default_rec.date,
    #                 "e_date": default_rec.e_date,
    #                 "tea_connect": [(6, 0, default_rec.tea_connect.ids)],
    #             }
    #         )
    #     return res
