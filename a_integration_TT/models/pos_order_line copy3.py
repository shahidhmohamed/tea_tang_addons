# all waorking but batch no is replacing for all
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


class TeaOrderLine(models.Model):
    _name = "tea.order.line"

    tea_tang_line_conn = fields.Many2one("tea.order.new")
    custom_name = fields.Char(string="CUSTOM NAME")
    session_id = fields.Integer(string="ID")
    full_product_name = fields.Char(string="FULL PRODUCT NAME")
    amount_total = fields.Float("AMOUNT TOTAL")
    product_id = fields.Integer(string="REF")
    ReceiptDate = fields.Datetime(
        string="RECEIPT DATE", default=lambda self: datetime.now()
    )
    ReceiptTime = fields.Char(string="RECEIPT TIME", compute="_compute_receipt_time")
    ReceiptNo = fields.Char(string="RECEIPT NO")
    NoOfItems = fields.Integer(string="NO OF ITEMS")
    SalesCurrency = fields.Char(string="SALESCURRENCY")
    TotalSalesAmtB4Tax = fields.Float(string="TOTAL SALES B4 TAX")
    TotalSalesAmtAfterTax = fields.Float(string="TOTAL SLAES AMT AFTER TAX")
    # SalesTaxRate = fields.Float(string ="TAX", compute ="_compute_tax_rate")
    ServiceChargeAmt = fields.Integer(string="SERVICE CHARGE AMT")
    PaymentAmt = fields.Integer(string="PAYMENT AMT")
    PaymentCurrency = fields.Char(string="PAYMENT CURRENCY")
    PaymentMethods = fields.Char(string="PAYMENT METHOD")
    # SalesType = fields.Char(string ="SALES TYPE")
    ItemDesc = fields.Char(string="ITEM DESC")
    ItemAmt = fields.Float(string="ITEM AMT")
    ItemDiscoumtAmt = fields.Integer(string="ITEM DISCOUNT AMT")
    order_id = fields.Integer(string="ORDER ID")
    company = fields.Char(string="COMPANY")
    status = fields.Char(string="STATUS", default="Open")
    batch = fields.Char(string="BATCH")
    UnitPrice = fields.Float("PRICE UNIT")
    AmtTax = fields.Float("AMOUNT TOTAL TAX")

    # TotalTax = fields.Float(string="TOTAL TAX", compute="_compute_total_tax")

    # @api.depends('session_id', 'SalesTaxRate')
    # def _compute_total_tax(self):
    #     for record in self:
    #         if record.session_id:
    #             # Filter tea order lines with the same session_id
    #             lines_with_same_session_id = self.filtered(lambda r: r.session_id == record.session_id)
    #             # Sum up the total tax from these lines
    #             total_tax = sum(line.SalesTaxRate for line in lines_with_same_session_id)
    #             record.TotalTax = total_tax
    #         else:
    #             record.TotalTax = 0.0

    SalesType = fields.Char(
        string="SALES TYPE", compute="_compute_negative_total_sales", store=True
    )

    @api.depends("TotalSalesAmtAfterTax")
    def _compute_negative_total_sales(self):
        for record in self:
            if record.TotalSalesAmtAfterTax < 0:
                record.SalesType = "Return"
            else:
                record.SalesType = "Sales"

    session_count = fields.Integer(
        string="NO ITEM TOTAL ITEM", compute="_compute_session_count", store=True
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

    # @api.depends('TotalSalesAmtB4Tax', 'TotalSalesAmtAfterTax')
    # def _compute_tax_rate(self):
    #     for record in self:
    #         if record.TotalSalesAmtB4Tax and record.TotalSalesAmtAfterTax:
    #             tax_rate = record.TotalSalesAmtAfterTax - record.TotalSalesAmtB4Tax
    #             record.SalesTaxRate = tax_rate
    #         else:
    #             record.SalesTaxRate = 0.0

    @api.depends("AmtTax", "amount_total")
    def _compute_b4_tax_rate(self):
        for record in self:
            if record.AmtTax and record.amount_total:
                b4_tax_rate = record.amount_total - record.AmtTax
                record.TotalSalesAmtB4Tax = b4_tax_rate
            else:
                record.TotalSalesAmtB4Tax = 0.0

    # @api.depends('NoOfItems', 'UnitPrice')
    # def _compute_amt(self):
    #     for record in self:
    #         if record.NoOfItems and record.UnitPrice:
    #             ItemAmt = record.NoOfItems * record.UnitPrice
    #             record.ItemAmt = ItemAmt
    #         else:
    #             record.ItemAmt = 0.0

    # def button_check(self):
    #     # Fetch records from the current model
    #     records = self.env['tea.order.line'].search_read([], ['full_product_name', 'ReceiptNo', 'session_id'])
    #     payment = self.env['tea.order.line.2'].search_read([], ['PaymentMethods', 'PaymentAmt'])

    #     # Structure the data into the desired JSON format
    #     json_data = {
    #         "AppCode": "POS-02",
    #         "PropertyCode": "CCB1",
    #         "ClientID": "CCB1-PS-20-000001",
    #         "ClientSecret": "S1D+qcjn47M=",
    #         "POSInterfaceCode": "CCB1-PS-20-000001",
    #         "BatchCode": "123",
    #         "PosSales": [],
    #     }

    #     for record in records:
    #         pos_sale = {
    #             "PropertyCode": "CCB1",
    #             "POSInterfaceCode": "CCB1-PS-20-000001",
    #             "amount_total": record["full_product_name"],
    #             "amount_paid": record["ReceiptNo"],
    #             "date_order": record["session_id"],
    #             "PaymentMethods": ,
    #         }
    #         json_data["PosSales"].append(pos_sale)

    #     # Convert JSON data to a string
    #     json_data_str = json.dumps(json_data, indent=4)

    #     # Raise UserError with the JSON data string
    #     raise exceptions.UserError(json_data_str)

    def button_check(self):
        # Convert current datetime
        india_timezone = timezone("Asia/Colombo")
        india_time = datetime.now(india_timezone)
        # Format the datetime into BatchCode format without colons
        batch_code = india_time.strftime("%d%m%Y%H%M%S")
        # Fetch records from the current model where status is blank
        records = self.env["tea.order.line"].search([("status", "=", "Open")])
        # Initialize the json_data dictionary
        if records:
            json_data = {
                "AppCode": "POS-02",
                "PropertyCode": "CCB1",
                "ClientID": "CCB1-PS-23-00000063",
                "ClientSecret": "5TH8d9LY+mseoDEEG8T+OQ==",
                "POSInterfaceCode": "CCB1-PS-23-00000063",
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
                    "Tea Tang Boutique - One Galle Face Mall",
                    # "Tea Tang Boutique - Liberty Plaza",
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
            }

            for session_id, items in session_records.items():

                # Check if any of the items in the session have a status other than "Open"
                if any(item.status != "Open" for item in items):
                    continue  # Skip this session if any item has a status other than "Open"
                # receipt_no = items[0].ReceiptNo
                session_items = {
                    "PropertyCode": "CCB1",
                    "POSInterfaceCode": "CCB1-PS-23-00000063",
                    "ReceiptDate": items[0].ReceiptDate.strftime("%d/%m/%Y"),
                    # "ReceiptDate": "25/04/2024",
                    "ReceiptTime": items[0].ReceiptTime,
                    "ReceiptNo": items[0].ReceiptNo,
                    "NoOfItems": len(items),
                    "SalesCurrency": "LKR",
                    "TotalSalesAmtB4Tax": items[0].TotalSalesAmtB4Tax,
                    "TotalSalesAmtAfterTax": items[0].amount_total,
                    "SalesTaxRate": 5.00,
                    "ServiceChargeAmt": 0.00,
                    "PaymentAmt": 0.00,
                    "PaymentCurrency": "LKR",
                    "PaymentMethod": "",
                    # "SalesType": "Sales",
                    # "PaymentMethod": items[0].PaymentMethods,
                    "SalesType": items[0].SalesType,
                    "Items": [],
                }
                # Check if SalesType is "Return" and add "Cash" to PaymentMethod
                if items[0].SalesType == "Return":
                    session_items["PaymentMethod"] = "Cash"
                else:
                    # session_items["PaymentMethod"] = items[0].PaymentMethods
                    payment_methods = items[0].PaymentMethods.split(
                        ", "
                    )  # Split the payment methods
                    renamed_payment_methods = [
                        payment_method_mapping.get(method, method)
                        for method in payment_methods
                    ]  # rename
                    session_items["PaymentMethod"] = ", ".join(
                        renamed_payment_methods
                    )  # join

                # Fetch payments for this session
                session_payments = payments.filtered(
                    lambda p: p.session_id == session_id
                )
                for payment in session_payments:
                    payment_amt = payment.PaymentAmt
                    if payment_amt < 0:
                        payment_amt = abs(payment_amt)  # Convert negative to positive
                    session_items["PaymentAmt"] += payment_amt

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
                            "ItemDiscoumtAmt": 0.00,
                        }
                    )

                # Modify TotalSalesAmtB4Tax to ensure it's positive
                total_sales_b4_tax = session_items["TotalSalesAmtB4Tax"]
                if total_sales_b4_tax < 0:
                    total_sales_b4_tax = abs(
                        total_sales_b4_tax
                    )  # Convert negative to positive
                session_items["TotalSalesAmtB4Tax"] = total_sales_b4_tax

                # Modify TotalSalesAmtAfterTax to ensure it's positive
                total_sales_after_tax = session_items["TotalSalesAmtAfterTax"]
                if total_sales_after_tax < 0:
                    total_sales_after_tax = abs(
                        total_sales_after_tax
                    )  # Convert negative to positive
                session_items["TotalSalesAmtAfterTax"] = total_sales_after_tax

                # Add session_items to the Items list in json_data
                json_data["PosSales"].append(
                    session_items
                )  # Changed "PosSales" to "Items"
            # Convert JSON data to a string
            json_data_str = json.dumps(json_data, indent=4)

            # raise exceptions.UserError(json_data_str)

            # Define client credentials
            client_id = "CCB1-PS-23-00000063"
            client_secret = "5TH8d9LY+mseoDEEG8T+OQ=="
            access_token_url = "https://d3dsrywsljg161.cloudfront.net/connect/token"
            data_url = "https://d3dsrywsljg161.cloudfront.net/api/possale/importpossaleswithitems"

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
                        # if response_data.get("returnStatus") == "Failed":
                        for record in records_to_send:
                            record.write(
                                {
                                    "status": "Success",
                                    "batch": response_data.get("batchCode"),
                                }
                            )
                    else:
                        # raise exceptions.UserError(response.text)
                        for record in records_to_send:
                            record.write({"status": "Open"})

                else:
                    # Update records with Open status
                    for record in records_to_send:
                        record.write({"status": "Open"})
                    raise exceptions.UserError("Error: Failed to import POS sales data")
            # raise exceptions.UserError(json_data_str)
            else:
                raise exceptions.UserError("Error: Failed to obtain access token")
        else:
            # If no records with blank status, raise an exception
            raise exceptions.UserError("Error: No records found with blank status")
