from odoo import models, fields, api, _
from odoo.exceptions import UserError


class TeaOrder(models.Model):
    _name = "tea.order.new"

    custom_name = fields.Char(string="Custom Name")
    pos_connect = fields.One2many("tea.order.line", "tea_tang_line_conn")
    pos_connect_lien_2 = fields.One2many("tea.order.line.2", "tea_tang_line_conn_2")
    session_id = fields.Integer(string="id")

    # def get_data(self):
    #     pos_orders = self.env['pos.order'].search([])
    #     for record in pos_orders:
    #         UserError("Get Data", record.id)

    # def get_data(self):
    #     pos = self.env['pos.order.line']
    #     data = pos.search([])

    #     order_line_value = []
    #     for record in data:
    #         # Populate po_line_values for each record
    #         po_line_values = {
    #             # mY field                 pos_field
    #             'session_id': record.id,
    #         }
    #         order_line_value.append((0, 0, po_line_values))
    #         data_fetched = True

    #     if data_fetched:
    #         # Update the get_po_lines field with the list of po_line_values
    #         self.pos_connect = order_line_value

    # def get_data(self):
    #     pos_order_lines = self.env['pos.order.line'].search([])
    #     tea_order_line = self.env['tea.order.line']  # Replace 'tea.order.line' with your actual model name

    #     for line in pos_order_lines:
    #         # Assuming 'tea.order.line' has a field named 'session_id' to store the 'id' from pos.order.line
    #         tea_order_line.create({'session_id': line.order_id})

    #     # After creating all records, commit the changes to the database
    #     self.env.cr.commit()

    # def get_data(self):
    #     pos_order_lines = self.env['pos.order.line'].search([])
    #     tea_order_line = self.env['tea.order.line']

    #     for line in pos_order_lines:
    #         # Check if a record with the same session_id already exists in tea.order.line
    #         existing_record = tea_order_line.search([('session_id', '=', line.order_id.id)])
    #         if not existing_record:
    #             # Create a new record only if it doesn't already exist
    #             tea_order_line.create({'session_id': line.order_id.id})

    #     # After creating all records, commit the changes to the database
    #     self.env.cr.commit()

    # def get_data(self):
    #     tea_order_line = self.env['tea.order.line']

    #     # Get the set of already processed session_ids
    #     processed_session_ids = {record.session_id for record in tea_order_line.search([])}

    #     # Fetch new data from pos.order.line excluding already processed session_ids
    #     new_pos_order_lines = self.env['pos.order.line'].search([('order_id', 'not in', list(processed_session_ids))])

    #     # Process new data
    #     for line in new_pos_order_lines:
    #         # Include additional fields as needed along with 'session_id'
    #         tea_order_line.create({
    #             'session_id': line.order_id.id,
    #             'custom_name': line.name,
    #             'full_product_name': line.full_product_name,
    #             'ReceiptDate': line.create_date,
    #             'TotalSalesAmtB4Tax': line.price_subtotal,
    #             'TotalSalesAmtAfterTax': line.price_subtotal_incl,
    #             'order_id': line.order_id,
    #             'NoOfItems': line.qty,
    #         })

    #     # After creating all records, commit the changes to the database
    #     self.env.cr.commit()

    # def get_data(self):
    #     tea_order_line = self.env['tea.order.line']

    #     # Get the set of already processed session_ids
    #     processed_session_ids = {record.session_id for record in tea_order_line.search([])}

    #     # Fetch new data from pos.order.line excluding already processed session_ids
    #     new_pos_order_lines = self.env['pos.order.line'].search([('order_id', 'not in', list(processed_session_ids))])

    #     # Process new data
    #     for line in new_pos_order_lines:
    #         # Fetch the corresponding pos.order record using the order_id from pos.order.line
    #         order = self.env['pos.order'].browse(line.order_id.id)
    #         # Include additional fields as needed along with 'session_id'
    #         tea_order_line.create({
    #             'session_id': line.order_id.id,
    #             'custom_name': line.name,
    #             'full_product_name': line.full_product_name,
    #             'ReceiptDate': line.create_date,
    #             'TotalSalesAmtB4Tax': line.price_subtotal,
    #             'TotalSalesAmtAfterTax': line.price_subtotal_incl,
    #             'order_id': line.order_id,
    #             'NoOfItems': line.qty,
    #             'company': line.company_id.name,
    #             # Fetch the ReceiptNo from pos.order model using the order object
    #             'ReceiptNo': order.pos_reference,
    #             'amount_total': order.amount_total,
    #         })

    #     # After creating all records, commit the changes to the database
    #     self.env.cr.commit()
    """
    Final Working start
    """
    # def get_data(self):
    #     tea_order_line = self.env['tea.order.line']
    #     tea_order_line_2 = self.env['tea.order.line.2']

    #     # Get the set of already processed session_ids
    #     processed_session_ids = {record.session_id for record in tea_order_line.search([])}

    #     # Fetch new data from pos.order.line excluding already processed session_ids
    #     new_pos_order_lines = self.env['pos.order.line'].search([('order_id', 'not in', list(processed_session_ids))])

    #     # Process new data
    #     for line in new_pos_order_lines:
    #         # Fetch the corresponding pos.order record using the order_id from pos.order.line
    #         order = self.env['pos.order'].browse(line.order_id.id)

    #         # Fetch payment data from pos_payment based on pos_order_id
    #         payments = self.env['pos.payment'].search([('id', '=', line.order_id.id)])

    #         # Get the payment methods
    #         payment_methods = []
    #         for payment in payments:
    #             payment_methods.append(payment.payment_method_id.name)

    #         # Include additional fields as needed along with 'session_id'
    #         tea_order_line.create({
    #             'session_id': line.order_id.id,
    #             'custom_name': line.name,
    #             'full_product_name': line.full_product_name,
    #             'ReceiptDate': line.create_date,
    #             'TotalSalesAmtB4Tax': line.price_subtotal,
    #             'TotalSalesAmtAfterTax': line.price_subtotal_incl,
    #             # 'SalesTaxRate': line.price_subtotal_incl,
    #             'order_id': line.order_id,
    #             'NoOfItems': line.qty,
    #             'company': line.company_id.name,
    #             # Fetch the ReceiptNo from pos.order model using the order object
    #             'ReceiptNo': order.pos_reference,
    #             'amount_total': order.amount_total,
    #             # Include payment method data
    #             'PaymentMethods': ', '.join(payment_methods),  # Concatenate payment methods if multiple
    #         })

    #         tea_order_line_2.create({
    #             'PaymentAmt': payment.amount,
    #             'ReceiptNo': order.pos_reference,
    #             'company': line.company_id.name,
    #             'ReceiptDate': line.create_date,
    #             'session_id': line.order_id.id,
    #             'cardtype': payment.card_type,
    #             'company': line.company_id.name,
    #             'PaymentMethods': ', '.join(payment_methods),  # Concatenate payment methods if multiple
    #         })

    #     # After creating all records, commit the changes to the database
    #     self.env.cr.commit()
    """
    Final Working end
    """

    def get_data(self):
        tea_order_line = self.env["tea.order.line"]
        tea_order_line_2 = self.env["tea.order.line.2"]

        # Get the set of already processed session_ids
        processed_session_ids = {
            record.session_id for record in tea_order_line.search([])
        }

        # Fetch new data from pos.order.line excluding already processed session_ids
        new_pos_order_lines = self.env["pos.order.line"].search(
            [("order_id", "not in", list(processed_session_ids))]
        )

        # Create a dictionary to track processed session ids
        processed_sessions = {}

        # Process new data
        for line in new_pos_order_lines:
            # Fetch the corresponding pos.order record using the order_id from pos.order.line
            order = self.env["pos.order"].browse(line.order_id.id)

            # Fetch payment data from pos_payment based on pos_order_id
            payments = self.env["pos.payment"].search(
                [("pos_order_id", "=", line.order_id.id)]
            )

            # Get the payment methods
            payment_methods = []
            for payment in payments:
                payment_methods.append(payment.payment_method_id.name)

            # Include additional fields as needed along with 'session_id'
            tea_order_line.create(
                {
                    "session_id": line.order_id.id,
                    "custom_name": line.name,
                    "full_product_name": line.full_product_name,
                    "ReceiptDate": line.create_date,
                    "TotalSalesAmtB4Tax": line.price_subtotal,
                    "TotalSalesAmtAfterTax": order.amount_total,
                    "order_id": line.order_id,
                    "ItemAmt": line.price_subtotal_incl,
                    "AmtTax": order.amount_tax,
                    "NoOfItems": line.qty,
                    "UnitPrice": line.price_unit,
                    "company": line.company_id.name,
                    "ReceiptNo": order.pos_reference,
                    "amount_total": order.amount_total,
                    "PaymentMethods": ", ".join(payment_methods),
                }
            )

            # Create record in tea_order_line_2 only if session_id is not already processed
            if line.order_id.id not in processed_sessions:
                for payment in payments:
                    tea_order_line_2.create(
                        {
                            "PaymentAmt": payment.amount,
                            "ReceiptNo": order.pos_reference,
                            "company": line.company_id.name,
                            "ReceiptDate": line.create_date,
                            "session_id": line.order_id.id,
                            "cardtype": payment.card_type,
                            "PaymentMethods": payment.payment_method_id.name,
                            "SalesType": payment.name,
                        }
                    )
                # Mark session_id as processed
                processed_sessions[line.order_id.id] = True

        # After creating all records, commit the changes to the database
        self.env.cr.commit()

    # def get_data(self):
    #     tea_order_line_obj = self.env['tea.order.line']
    #     other_table_obj = self.env['tea.order.line.2']

    #     # Get the set of already processed session_ids
    #     processed_session_ids = {record.session_id for record in tea_order_line_obj.search([])}

    #     # Fetch new data from pos.order.line excluding already processed session_ids
    #     new_pos_order_lines = self.env['pos.order.line'].search([('order_id', 'not in', list(processed_session_ids))])

    #     # Process new data
    #     for line in new_pos_order_lines:
    #         # Fetch the corresponding pos.order record using the order_id from pos.order.line
    #         order = self.env['pos.order'].browse(line.order_id.id)

    #         # Fetch payment data from pos_payment based on pos_order_id
    #         payments = self.env['pos.payment'].search([('pos_order_id', '=', order.id)])

    #         # Get the payment methods
    #         payment_methods = []
    #         for payment in payments:
    #             payment_methods.append(payment.payment_method_id.name)

    #         # Create a record in the tea.order.line table with the required data
    #         tea_order_line_obj.create({
    #             'session_id': line.order_id.id,
    #             'custom_name': line.name,
    #             'full_product_name': line.full_product_name,
    #             # 'receipt_date': line.create_date,
    #             'total_sales_amt_b4_tax': line.price_subtotal,
    #             'total_sales_amt_after_tax': line.price_subtotal_incl,
    #             'order_id': line.order_id.id,
    #             'no_of_items': line.qty,
    #             'company': line.company_id.name,
    #             'receipt_no': order.pos_reference,
    #             'amount_total': order.amount_total,
    #             # Add other fields as needed
    #         })

    #         # Create a record in the other table with the payment methods
    #         other_table_obj.create({
    #             'session_id': line.order_id.id,
    #             'payment_methods': ', '.join(payment_methods),  # Concatenate payment methods if multiple
    #             # Add other fields as needed
    #         })

    #     # After creating all records, commit the changes to the database
    #     self.env.cr.commit()
