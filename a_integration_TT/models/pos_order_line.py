from odoo import models, fields, api, exceptions, _
from pytz import timezone
from datetime import datetime
import json
import xmlrpc.client
import requests
from collections import defaultdict
import xml.etree.ElementTree as ET
import os
from .xml_utils import dict_to_xml


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    TaxRate = fields.Float(string="Tax Rate", compute="_get_tax_new", store=True)

    @api.depends("tax_ids_after_fiscal_position")
    def _get_tax_new(self):
        for record in self:
            if record.tax_ids_after_fiscal_position:
                record.TaxRate = record.tax_ids_after_fiscal_position.amount
            else:
                record.TaxRate = 0

    @api.model
    def create(self, vals):
        record = super(PosOrderLine, self).create(vals)
        record._update_tea_order_line()
        return record

    def _update_tea_order_line(self):
        tea_order_line = self.env["tea.order.line"]
        tea_order_line_2 = self.env["tea.order.line.2"]

        # Fetch the corresponding pos.order record using the order_id from pos.order.line
        order = self.env["pos.order"].browse(self.order_id.id)

        # Fetch payment data from pos_payment based on pos_order_id
        payments = self.env["pos.payment"].search(
            [("pos_order_id", "=", self.order_id.id)]
        )

        # Get the payment methods
        payment_methods = [payment.payment_method_id.name for payment in payments]

        # company list
        allowed_companies = [
            "Tea Tang - One Galle Face Mall",
            "SHA Foundation - One Galle Face Mall",
        ]

        # Check if the company name is in the allowed list
        if self.company_id.name in allowed_companies:

            # Create record in tea.order.line
            tea_order_line.create(
                {
                    "session_id": self.order_id.id,
                    "custom_name": self.name,
                    "full_product_name": self.full_product_name,
                    "ReceiptDate": self.create_date,
                    "TotalSalesAmtB4Tax": self.price_subtotal,
                    "TotalSalesAmtAfterTax": order.amount_total,
                    "order_id": self.order_id.id,
                    "ItemAmt": self.price_subtotal_incl,
                    "AmtTax": order.amount_tax,
                    "NoOfItems": self.qty,
                    "UnitPrice": self.price_unit,
                    "company": self.company_id.name,
                    "ReceiptNo": order.pos_reference,
                    "amount_total": order.amount_total,
                    "PaymentMethods": ", ".join(payment_methods),
                    "discountPercent": self.discount,
                    "TaxRate": self.TaxRate,
                }
            )

            # Create record in tea.order.line.2
            for payment in payments:
                tea_order_line_2.create(
                    {
                        "PaymentAmt": payment.amount,
                        "ReceiptNo": order.pos_reference,
                        "company": self.company_id.name,
                        "ReceiptDate": self.create_date,
                        "session_id": self.order_id.id,
                        "cardtype": payment.card_type,
                        "PaymentMethods": payment.payment_method_id.name,
                        "SalesType": payment.name,
                    }
                )


class TeaOrderLine(models.Model):
    _name = "tea.order.line"
    _order = "session_id desc"

    tea_tang_line_conn = fields.Many2one("tea.order.new")
    date_connect = fields.Many2one("date", string="DATE")
    date = fields.Datetime(string="DATE", related="date_connect.date")
    custom_name = fields.Char(string="Custom Name")
    session_id = fields.Integer(string="ID")
    full_product_name = fields.Char(string="Product Name")
    amount_total = fields.Float("Bill Total")
    product_id = fields.Integer(string="Ref")
    ReceiptDate = fields.Datetime(
        string="Receipt Date", default=lambda self: datetime.now()
    )
    ReceiptTime = fields.Char(string="Receipt Time", compute="_compute_receipt_time")
    ReceiptNo = fields.Char(string="Receipt No")
    SalesCurrency = fields.Char(string="Sales Currency")
    TotalSalesAmtB4Tax = fields.Float(string="Line Total Excl. tax")
    TotalSalesAmtAfterTax = fields.Float(string="Bill Total Incl. Tax")
    # SalesTaxRate = fields.Float(string ="TAX", compute ="_compute_tax_rate")
    ServiceChargeAmt = fields.Integer(string="Service Charge")
    PaymentAmt = fields.Integer(string="Payment Amount")
    PaymentCurrency = fields.Char(string="Payment Currency")
    PaymentMethods = fields.Char(string="Payment Method")
    # SalesType = fields.Char(string ="SALES TYPE")
    ItemDesc = fields.Char(string="Item Desc")
    ItemAmt = fields.Float(string="Line Total")
    ItemDiscoumtAmt = fields.Integer(string="Item Discount Amount")
    order_id = fields.Integer(string="Order ID")
    company = fields.Char(string="Company")
    status = fields.Char(string="Status", default="Open")
    batch = fields.Char(string="Batch")
    NoOfItems = fields.Integer(string="Quantity")
    UnitPrice = fields.Float("Unit Price")
    AmtTax = fields.Float("Tax Amount")
    TaxRate = fields.Float(string="Tax %", store=True)
    SentTime = fields.Char(string="Response Time")
    QtyUnitPrice = fields.Float(
        string="Qty UnitPrice", compute="_compute_qty_unit_price", store=True
    )
    discountPercent = fields.Integer(string="Discount %", default=0)
    itemDiscount = fields.Float(
        string="Discount Amount", compute="_compute_item_discount", store=True
    )

    @api.depends("NoOfItems", "UnitPrice")
    def _compute_qty_unit_price(self):
        for record in self:
            record.QtyUnitPrice = record.NoOfItems * record.UnitPrice

    @api.depends("QtyUnitPrice", "discountPercent")
    def _compute_item_discount(self):
        for record in self:
            record.itemDiscount = abs(
                record.QtyUnitPrice * (record.discountPercent / 100.0)
            )

    SalesType = fields.Char(
        string="Sales Type", compute="_compute_negative_total_sales", store=True
    )

    @api.depends("TotalSalesAmtAfterTax")
    def _compute_negative_total_sales(self):
        for record in self:
            if record.TotalSalesAmtAfterTax < 0:
                record.SalesType = "Return"
            else:
                record.SalesType = "Sales"

    session_count = fields.Integer(
        string="Total No of Items", compute="_compute_session_count", store=True
    )

    order_line_count = fields.Integer(
        string="Total No of Lines", compute="_compute_session_count", store=True
    )

    @api.depends("session_id")
    def _compute_session_count(self):
        # Count the occurrences of each session_id in the database
        session_count_data = self.env["tea.order.line"].read_group(
            [("session_id", "!=", False)], ["session_id"], ["session_id"]
        )
        session_count_dict = {
            data["session_id"]: data["session_id_count"] for data in session_count_data
        }

        # Update the session_count field for each record
        for record in self:
            record.session_count = session_count_dict.get(record.session_id, 0)
            record.order_line_count = session_count_dict.get(record.session_id, 0)

    @api.depends("ReceiptDate")
    def _compute_receipt_time(self):
        for record in self:
            if record.ReceiptDate:
                # Convert ReceiptDate to the local time zone 'Asia/Colombo'
                local_time = record.ReceiptDate.astimezone(timezone("Asia/Colombo"))
                # Format the local time as string
                receipt_time = local_time.strftime("%H:%M:%S")
                record.ReceiptTime = receipt_time
            else:
                record.ReceiptTime = False

    @api.depends("AmtTax", "amount_total")
    def _compute_b4_tax_rate(self):
        for record in self:
            if record.AmtTax and record.amount_total:
                b4_tax_rate = record.amount_total - record.AmtTax
                record.TotalSalesAmtB4Tax = b4_tax_rate
            else:
                record.TotalSalesAmtB4Tax = 0.0

    # new
    def button_check(self):

        # Fetch credentials from tea.credentials model
        credentials = self.env["tea.credentials"].search([], limit=1)
        if not credentials:
            raise exceptions.userError("Tea Tag - OGF Credentials not found.")

        client_id = credentials.customer_id
        client_secret = credentials.secret_client
        access_token_url = credentials.token_url
        data_url = credentials.ogf_url
        app_code = credentials.app_code
        property_code = credentials.property_code

        # Convert current datetime
        india_timezone = timezone("Asia/Colombo")
        india_time = datetime.now(india_timezone)
        # Format the datetime into BatchCode format without colons
        batch_code = india_time.strftime("%d%m%Y%H%M%S")

        # Fetch the date from the date model
        date_record = self.env["date"].search([], limit=1)

        if not date_record or not date_record.date:
            raise exceptions.UserError("Date not found in the date model.")
        # Convert the fetched date to a comparable datetime object
        # comparison_date = date_record.date
        start_date = date_record.date
        end_date = date_record.e_date

        # Fetch records from the current model where status is blank testing
        records = self.env["tea.order.line"].search(
            [
                ("status", "=", "Open"),
                ("ReceiptDate", ">=", start_date),
                ("ReceiptDate", "<=", end_date),
            ]
        )
        # Initialize the json_data dictionary
        if records:
            json_data = {
                "AppCode": app_code,
                "PropertyCode": property_code,
                "ClientID": client_id,
                # "ClientID": "CCB1-PS-23-000000631",
                "ClientSecret": client_secret,
                "POSInterfaceCode": client_id,
                "BatchCode": batch_code,
                "PosSales": [],
            }
            # Fetch records from the current model
            records = self.env["tea.order.line"].search(
                []
            )  # Fetch all records from tea.order.line
            payments = self.env["tea.order.line.2"].search(
                []
            )  # Fetch all records from tea.order.line.2
            records_to_send = []
            # Group records by session ID
            session_records = defaultdict(list)
            for record in records:
                if record.company in [
                    "Tea Tang - One Galle Face Mall",
                    "SHA Foundation - One Galle Face Mall",
                ]:
                    session_records[record.session_id].append(record)
                    records_to_send.append(record)

            # Define a dictionary to map payment methods to their desired names
            payment_method_mapping = {
                "CASH": "Cash",
                "CC OTHER": "Credit Card",
                "CC AMEX": "Credit Card",
                "CC MASTER": "Credit Card",
                "CC VISA": "Credit Card",
                "Bank": "Credit Card",
                "GIFT VOUCHER OGF": "Voucher",
            }
            # Keep track of records processed in the current run
            processed_record_ids = set()

            for session_id, items in session_records.items():

                # Check if any of the items in the session have a status other than "Open"
                if any(item.status != "Open" for item in items):
                    continue  # Skip this session if any item has a status other than "Open"

                session_items = {
                    "PropertyCode": property_code,
                    "POSInterfaceCode": client_id,
                    "ReceiptDate": items[0].ReceiptDate.strftime("%d/%m/%Y"),
                    # "ReceiptDate": "25/04/2024",
                    "ReceiptTime": items[0].ReceiptTime,
                    "ReceiptNo": items[0].ReceiptNo,
                    "NoOfItems": len(items),
                    "SalesCurrency": "LKR",
                    "TotalSalesAmtB4Tax": items[0].TotalSalesAmtB4Tax,
                    "TotalSalesAmtAfterTax": items[0].amount_total,
                    "SalesTaxRate": 18.00,
                    "ServiceChargeAmt": 0.00,
                    # "PaymentAmt": 0.00,
                    "PaymentAmt": items[0].amount_total,
                    "PaymentCurrency": "LKR",
                    "PaymentMethod": "",
                    # "SalesType": "Sales",
                    # "PaymentMethod": items[0].PaymentMethods,
                    "SalesType": items[0].SalesType,
                    "Items": [],
                }
                unique_payment_methods = set()

                for item in items:
                    payment_methods = item.PaymentMethods.split(", ")
                    unique_payment_methods.update(payment_methods)

                session_payments = payments.filtered(
                    lambda p: p.session_id == session_id
                )
                for payment in session_payments:
                    unique_payment_methods.add(payment.PaymentMethods)

                payment_method_list = list(unique_payment_methods)
                renamed_payment_methods = [
                    payment_method_mapping.get(method, method)
                    for method in payment_method_list
                ]
                renamed_payment_methods = [
                    method for method in renamed_payment_methods if method.strip()
                ]
                payment_method_str = ", ".join(renamed_payment_methods)
                session_items["PaymentMethod"] = payment_method_str

                # Add items to the session_items dictionary
                for item in items:
                    item_amt = item.ItemAmt
                    if item_amt < 0:
                        item_amt = abs(item_amt)  # Convert negative to positive

                    # Add item details to the Items list
                    session_items["Items"].append(
                        {
                            "ItemDesc": item.full_product_name,
                            # "ItemAmt": item.ItemAmt,
                            "ItemAmt": item_amt,
                            "ItemDiscoumtAmt": item.itemDiscount,
                        }
                    )

                # Modify TotalSalesAmtB4Tax to ensure it's positive
                total_sales_b4_tax = session_items["TotalSalesAmtB4Tax"]
                if total_sales_b4_tax < 0:
                    total_sales_b4_tax = abs(
                        total_sales_b4_tax
                    )  # Convert negative to positive
                session_items["TotalSalesAmtB4Tax"] = total_sales_b4_tax

                # Modify TotalSalesAmtAfterTax and PaymentAmt to ensure it's positive
                total_sales_after_tax = session_items["TotalSalesAmtAfterTax"]
                if total_sales_after_tax < 0:
                    total_sales_after_tax = abs(
                        total_sales_after_tax
                    )  # Convert negative to positive
                session_items["TotalSalesAmtAfterTax"] = total_sales_after_tax

                paidAmount = session_items["PaymentAmt"]
                if paidAmount < 0:
                    paidAmount = abs(paidAmount)  # Convert negative to positive
                session_items["PaymentAmt"] = paidAmount

                # Add session_items to the Items list in json_data
                json_data["PosSales"].append(
                    session_items
                )  # Changed "PosSales" to "Items"

                # Add processed record IDs to the set
                processed_record_ids.update(item.id for item in items)
            # Convert JSON data to a string
            json_data_str = json.dumps(json_data, indent=4)

            raise exceptions.UserError(json_data_str)

            # Make a POST request to get the access token
            payload = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = requests.post(access_token_url, data=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Extract the access token from the response
                access_token = response.json()["access_token"]
                # Make a POST request to post the data to the specified URL
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                }
                response = requests.post(data_url, data=json_data_str, headers=headers)
                if response.status_code == 200:
                    response_data = response.json()
                    if response_data.get("returnStatus") == "Success":
                        sent_time = datetime.now(india_timezone).strftime(
                            "%d/%m/%Y %H:%M:%S"
                        )
                        # if response_data.get("returnStatus") == "Failed":
                        for record in records_to_send:
                            if record.id in processed_record_ids:
                                record.write(
                                    {
                                        "status": "Success",
                                        "batch": response_data.get("batchCode"),
                                        "SentTime": sent_time,
                                    }
                                )
                    else:
                        # raise exceptions.UserError(response.text)
                        for record in records_to_send:
                            if record.id in processed_record_ids:
                                record.write({"status": "Open"})

                else:
                    # Update records with Open status
                    for record in records_to_send:
                        if record.id in processed_record_ids:
                            record.write({"status": "Open"})

                    raise exceptions.UserError("Error: Failed to import POS sales data")
            # raise exceptions.UserError(json_data_str)
            else:
                raise exceptions.UserError("Error: Failed to obtain access token")
        else:
            # If no records with blank status, raise an exception
            raise exceptions.UserError("Error: No records found with blank status")


# tested working
