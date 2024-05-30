from odoo import models, fields, api, exceptions, _
from pytz import timezone
from datetime import datetime
import json
import xmlrpc.client
import requests
from collections import defaultdict


class TeaOrderLine(models.Model):
    _name = "tea.order.line"

    tea_tang_line_conn = fields.Many2one("tea.order.new")
    custom_name = fields.Char(string="CUSTOM NAME")
    session_id = fields.Integer(string="ID")
    full_product_name = fields.Char(string="FULL PRODUCT NAME")
    amount_total = fields.Float("AMOUNT TOTAL")
    product_id = fields.Char(string="REF")
    ReceiptDate = fields.Date(string="RECEIPT DATE")
    ReceiptTime = fields.Date(string="RECEIPT TIME", compute="_compute_receipt_time")
    ReceiptNo = fields.Char(string="RECEIPT NO")
    NoOfItems = fields.Integer(string="NO OF ITEMS")
    SalesCurrency = fields.Char(string="SALESCURRENCY")
    TotalSalesAmtB4Tax = fields.Float(string="TOTAL SALES B4 TAX")
    TotalSalesAmtAfterTax = fields.Float(
        string="TOTAL SLAES AMT AFTER TAX TotalSalesAmtAfterTax"
    )
    SalesTaxRate = fields.Float(string="TAX", compute="_compute_tax_rate")
    ServiceChargeAmt = fields.Integer(string="SERVICE CHARGE AMT")
    PaymentAmt = fields.Integer(string="PAYMENT AMT")
    PaymentCurrency = fields.Char(string="PAYMENT CURRENCY")
    PaymentMethods = fields.Char(string="PAYMENT METHOD")
    SalesType = fields.Char(string="SALES TYPE")
    ItemDesc = fields.Char(string="ITEM DESC")
    ItemAmt = fields.Integer(string="ITEM AMT")
    ItemDiscoumtAmt = fields.Integer(string="ITEM DISCOUNT AMT")
    order_id = ItemAmt = fields.Integer(string="ORDER ID")
    company = fields.Char(string="COMPANY")
    status = fields.Char(string="STATUS")

    @api.depends("ReceiptDate")
    def _compute_receipt_time(self):
        for record in self:
            if record.ReceiptDate:
                # Extract time part from ReceiptDate and format it as string
                receipt_time = record.ReceiptDate.strftime("%Y-%m-%d %H:%M:%S")
                record.ReceiptTime = receipt_time
            else:
                record.ReceiptTime = False

    @api.depends("TotalSalesAmtB4Tax", "TotalSalesAmtAfterTax")
    def _compute_tax_rate(self):
        for record in self:
            if record.TotalSalesAmtB4Tax and record.TotalSalesAmtAfterTax:
                tax_rate = record.TotalSalesAmtAfterTax - record.TotalSalesAmtB4Tax
                record.SalesTaxRate = tax_rate
            else:
                record.SalesTaxRate = 0.0

    def button_check(self):
        # Initialize the json_data dictionary
        json_data = {
            "AppCode": "POS-02",
            "PropertyCode": "CCB1",
            "ClientID": "CCB1-PS-23-00000063",
            "ClientSecret": "5TH8d9LY+mseoDEEG8T+OQ==",
            "POSInterfaceCode": "CCB1-PS-23-00000063",
            "BatchCode": "2024031913302760",
            "PosSales": [],
        }

        # Fetch records from the current model
        records = self.env["tea.order.line"].search(
            []
        )  # Fetch all records from tea.order.line
        payments = self.env["tea.order.line.2"].search(
            []
        )  # Fetch all records from tea.order.line.2

        # Group records by session ID
        session_records = defaultdict(list)
        for record in records:
            session_records[record.session_id].append(record)

        for session_id, items in session_records.items():
            # Initialize the pos_sale dictionary for the session
            receipt_no = items[0].ReceiptNo
            pos_sale = {
                "PropertyCode": "CCB1",
                "POSInterfaceCode": "CCB1-PS-23-00000063",
                "ReceiptDate": "19/12/2023",
                "ReceiptTime": "13:19:40",
                "ReceiptNo": receipt_no,
                "NoOfItems": 2,
                "SalesCurrency": "LKR",
                "TotalSalesAmtB4Tax": 500.00,
                "TotalSalesAmtAfterTax": 525.00,
                "SalesTaxRate": 5.00,
                "ServiceChargeAmt": 0.00,
                "PaymentAmt": 525.00,
                "PaymentCurrency": "LKR",
                "PaymentMethod": "Cash",
                "SalesType": "Sales",
                "ReceiptNo": items[
                    0
                ].ReceiptNo,  # Assuming ReceiptNo is the same for all items in the session
                # Add other common fields here
                "Items": [],
            }
            # Add items to the pos_sale dictionary
            for item in items:
                # Add item details to the Items list
                pos_sale["Items"].append(
                    {
                        # "ItemDesc": item.full_product_name,
                        "ItemDesc": "Apple",
                        "ItemAmt": 300.00,
                        "ItemDiscoumtAmt": 0.00,
                    }
                )

            # Add pos_sale to the PosSales list in json_data
            json_data["PosSales"].append(pos_sale)

        json_data_str = json.dumps(json_data, indent=4)

        # Define client credentials
        client_id = "CCB1-PS-23-00000063"
        client_secret = "5TH8d9LY+mseoDEEG8T+OQ=="
        access_token_url = "https://mims.imonitor.center/connect/token"
        data_url = "https://mims.imonitor.center/api/possale/importpossaleswithitems"

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
                if response_data.get("returnStatus") == "FAIL":
                    for record in records:
                        record.write({"status": "fail"})
                else:
                    raise exceptions.UserError(response.text)
            else:
                raise exceptions.UserError("Error: Failed to import POS sales data")
        # raise exceptions.UserError(json_data_str)
        else:
            raise exceptions.UserError("Error: Failed to obtain access token")
