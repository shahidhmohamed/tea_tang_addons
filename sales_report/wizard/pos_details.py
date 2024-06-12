from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class SaleDetails(models.TransientModel):
    _name = 'sale.details.wizard'
    _description = 'Sale Details Report'

    start_date = fields.Datetime(required=True, default=lambda self: fields.Datetime.now() - timedelta(days=2))
    end_date = fields.Datetime(required=True, default=lambda self: fields.Datetime.now())
    move_names = fields.Char(string='Move Names', compute='_compute_move_names')
    payment_dates = fields.Date(string='Payment Date')

    @api.depends('move_names')
    def _compute_payment_dates(self):
        for record in self:
            if record.move_names:
                payment = self.env['account.payment.register'].search([('communication', 'in', record.move_names.split('\n'))], limit=1)
                record.payment_dates = payment.date if payment else False
            else:
                record.payment_dates = False

    @api.depends('start_date', 'end_date')
    def _compute_move_names(self):
        for record in self:
            record.move_names = self._get_account_move_names(record.start_date, record.end_date)

    def _get_account_move_names(self, start_date, end_date):
        """
        Fetch the `name` field from `account.move` table based on the given date range.
        """
        self.env.cr.execute("""
            SELECT name
            FROM account_move
            WHERE date BETWEEN %s AND %s
        """, (start_date, end_date))
        result = self.env.cr.dictfetchall()
        names = [res['name'] for res in result]
        return '\n'.join(names)

    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    def generate_report(self):
        """
        Generate a report based on the selected date range and fetched data from account.move.
        """
        data = {
            'date_start': self.start_date,
            'date_stop': self.end_date,
            'payment_dates': self.payment_dates,
            'move_names': self.move_names.split('\n') if self.move_names else [],  # Split the string into a list
        }
        return self.env.ref('sales_report.action_sale_details_print').report_action([], data=data)

# class SaleDetails(models.TransientModel):
#     _name = 'sale.details.wizard'
#     _description = 'Sale Details Report'

#     start_date = fields.Datetime(required=True, default=lambda self: fields.Datetime.now() - timedelta(days=2))
#     end_date = fields.Datetime(required=True, default=fields.Datetime.now)
#     move_names = fields.Char(string='Move Names', compute='_compute_move_names')

#     @api.depends('start_date', 'end_date')
#     def _compute_move_names(self):
#         for record in self:
#             record.move_names = self._get_account_move_names(record.start_date, record.end_date)

#     def _get_account_move_names(self, start_date, end_date):
#         """
#         Fetch the `name` field from `account.move` table based on the given date range.
#         """
#         self.env.cr.execute("""
#             SELECT name
#             FROM account_move
#             WHERE date BETWEEN %s AND %s
#         """, (start_date, end_date))
#         result = self.env.cr.dictfetchall()
#         names = [res['name'] for res in result]
#         return '\n'.join(names)

#     @api.onchange('start_date', 'end_date')
#     def _onchange_dates(self):
#         if self.start_date and self.end_date and self.end_date < self.start_date:
#             self.end_date = self.start_date

#     def generate_report(self):
#         """
#         Generate a report based on the selected date range and fetched data from account.move.
#         """
#         data = {
#             'date_start': self.start_date,
#             'date_stop': self.end_date,
#             'move_names': self.move_names.split('\n') if self.move_names else [],  # Split the string into a list
#         }
#         return self.env.ref('sales_report.action_sale_details_print').report_action([], data=data)



    # def _default_start_date(self):
    #     """ Find the earliest start_date of the latests sessions """
    #     # restrict to configs available to the user
    #     config_ids = self.env['pos.config'].search([]).ids
    #     # exclude configs has not been opened for 2 days
    #     self.env.cr.execute("""
    #         SELECT
    #         max(start_at) as start,
    #         config_id
    #         FROM pos_session
    #         WHERE config_id = ANY(%s)
    #         AND start_at > (NOW() - INTERVAL '2 DAYS')
    #         GROUP BY config_id
    #     """, (config_ids,))
    #     latest_start_dates = [res['start'] for res in self.env.cr.dictfetchall()]
    #     # earliest of the latest sessions
    #     return latest_start_dates and min(latest_start_dates) or fields.Datetime.now()

    # start_date = fields.Datetime(required=True, default=_default_start_date)
    # end_date = fields.Datetime(required=True, default=fields.Datetime.now)
    # pos_config_ids = fields.Many2many('pos.config', 'pos_detail_configs',
    #     default=lambda s: s.env['pos.config'].search([]))

    # @api.onchange('start_date')
    # def _onchange_start_date(self):
    #     if self.start_date and self.end_date and self.end_date < self.start_date:
    #         self.end_date = self.start_date

    # @api.onchange('end_date')
    # def _onchange_end_date(self):
    #     if self.end_date and self.start_date and self.end_date < self.start_date:
    #         self.start_date = self.end_date

    # def generate_report(self):
    #     data = {'date_start': self.start_date, 'date_stop': self.end_date, 'config_ids': self.pos_config_ids.ids}
    #     return self.env.ref('sales_report.action_sale_details_print').report_action([], data=data)


'''
class SaleDetails(models.TransientModel):
    _name = 'sale.details.wizard'
    _description = 'Sale Details Report'

    start_date = fields.Datetime(required=True, default=lambda self: fields.Datetime.now() - timedelta(days=2))
    end_date = fields.Datetime(required=True, default=fields.Datetime.now)
    move_names = fields.Char(string='Move Names', compute='_compute_move_names')
    payment_dates = fields.Char(string='Payment Dates', compute='_compute_move_names')
    customer_names = fields.Char(string='Customer Names', compute='_compute_move_names')

    @api.depends('start_date', 'end_date')
    def _compute_move_names(self):
        for record in self:
            move_names, payment_dates, customer_names = self._get_account_move_details(record.start_date, record.end_date)
            record.move_names = move_names
            record.payment_dates = payment_dates
            record.customer_names = customer_names

    def _get_account_move_details(self, start_date, end_date):
        """
        Fetch details from `account.move` and related tables based on the given date range.
        """
        self.env.cr.execute("""
            SELECT name, partner_id
            FROM account_move
            WHERE date BETWEEN %s AND %s
        """, (start_date, end_date))
        result = self.env.cr.dictfetchall()

        move_names = [res['name'] for res in result]
        partner_ids = [res['partner_id'] for res in result]

        # Retrieve payment dates from account.payment.register
        payments = self.env['account.payment.register'].search([('communication', 'in', move_names)])
        payment_dates = {payment.communication: payment.payment_date.strftime('%Y-%m-%d') if payment.payment_date else 'N/A' for payment in payments}
        
        # Retrieve customer names
        partners = self.env['res.partner'].browse(partner_ids)
        customer_names = {partner.id: partner.name for partner in partners}

        # Prepare the combined data
        move_details = [
            {
                'name': name,
                'payment_date': payment_dates.get(name, 'N/A'),
                'customer_name': customer_names.get(partner_id, 'N/A')
            }
            for name, partner_id in zip(move_names, partner_ids)
        ]

        # Convert all items to strings to avoid TypeError
        move_names_str = '\n'.join(move_names)
        payment_dates_str = '\n'.join(str(value) for value in payment_dates.values())
        customer_names_str = '\n'.join(str(value) for value in customer_names.values())

        return move_names_str, payment_dates_str, customer_names_str

    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    def generate_report(self):
        """
        Generate a report based on the selected date range and fetched data from account.move.
        """
        data = {
            'date_start': self.start_date,
            'date_stop': self.end_date,
            'move_names': self.move_names.split('\n') if self.move_names else [],  # Split the string into a list
            'payment_dates': self.payment_dates.split('\n') if self.payment_dates else [],
            'customer_names': self.customer_names.split('\n') if self.customer_names else []
        }
        return self.env.ref('sales_report.action_sale_details_print').report_action([], data=data)
'''