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
    _name = 'tea.order.line'

    tea_tang_line_conn = fields.Many2one('tea.order.new')
    custom_name = fields.Char(string="CUSTOM NAME")
    session_id = fields.Integer(string="ID")
    full_product_name = fields.Char(string='FULL PRODUCT NAME')
    amount_total = fields.Float('AMOUNT TOTAL')
    product_id = fields.Integer(string='REF')
    ReceiptDate = fields.Datetime(string="RECEIPT DATE", default=lambda self: datetime.now())
    ReceiptTime = fields.Char(string = "RECEIPT TIME", compute ="_compute_receipt_time")
    ReceiptNo = fields.Char(string ="RECEIPT NO")
    NoOfItems = fields.Integer(string ="NO OF ITEMS")
    SalesCurrency = fields.Char(string='SALESCURRENCY')
    TotalSalesAmtB4Tax = fields.Float(string ="TOTAL SALES B4 TAX", compute ="_compute_b4_tax_rate")
    TotalSalesAmtAfterTax = fields.Float(string ="TOTAL SLAES AMT AFTER TAX")
    # SalesTaxRate = fields.Float(string ="TAX", compute ="_compute_tax_rate")
    ServiceChargeAmt = fields.Integer(string ="SERVICE CHARGE AMT")
    PaymentAmt = fields.Integer(string ="PAYMENT AMT")
    PaymentCurrency = fields.Char(string ="PAYMENT CURRENCY")
    PaymentMethods = fields.Char(string ="PAYMENT METHOD")
    # SalesType = fields.Char(string ="SALES TYPE")
    ItemDesc = fields.Char(string ="ITEM DESC")
    ItemAmt = fields.Float(string ="ITEM AMT")
    ItemDiscoumtAmt = fields.Integer(string ="ITEM DISCOUNT AMT")
    order_id = fields.Integer(string ="ORDER ID")
    company = fields.Char(string ="COMPANY")
    status = fields.Char(string ="STATUS")
    UnitPrice = fields.Float('PRICE UNIT')
    AmtTax = fields.Float('AMOUNT TOTAL TAX')

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

    SalesType = fields.Char(string="SALES TYPE", compute="_compute_negative_total_sales", store=True)

    @api.depends('TotalSalesAmtAfterTax')
    def _compute_negative_total_sales(self):
        for record in self:
            if record.TotalSalesAmtAfterTax < 0:
                record.SalesType = "Return"
            else:
                record.SalesType = "Sales"

    session_count = fields.Integer(string="NO ITEM TOTAL ITEM", compute='_compute_session_count', store=True)

    @api.depends('session_id')
    def _compute_session_count(self):
        # Count the occurrences of each session_id in the database
        session_count_data = self.env['tea.order.line'].read_group([('session_id', '!=', False)], ['session_id'], ['session_id'])
        session_count_dict = {data['session_id']: data['session_id_count'] for data in session_count_data}

        # Update the session_count field for each record
        for record in self:
            record.session_count = session_count_dict.get(record.session_id, 0)


    @api.depends('ReceiptDate')
    def _compute_receipt_time(self):
        for record in self:
            if record.ReceiptDate:
                # Convert ReceiptDate to the local time zone 'Asia/Colombo'
                local_time = record.ReceiptDate.astimezone(timezone('Asia/Colombo'))
                # Format the local time as string
                receipt_time = local_time.strftime('%H:%M:%S')
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
                
    @api.depends('AmtTax', 'amount_total')
    def _compute_b4_tax_rate(self):
        for record in self:
            if record.AmtTax and record.amount_total:
                b4_tax_rate = record.amount_total - record.AmtTax
                record.TotalSalesAmtB4Tax = b4_tax_rate
            else:
                record.TotalSalesAmtB4Tax = record.amount_total or 0.0

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
        # Initialize the json_data dictionary
        json_data = {
            "AppCode": "POS-02",
            "PropertyCode": "CCB1",
            "ClientID": "CCB1-PS-20-000001",
            "ClientSecret": "S1D+qcjn47M=",
            "POSInterfaceCode": "CCB1-PS-20-000001",
            "BatchCode": "123",
            "Items": [],  # Changed "PosSales" to "Items"
        }

        # Fetch records from the current model
        records = self.env['tea.order.line'].search([])  # Fetch all records from tea.order.line
        payments = self.env['tea.order.line.2'].search([])  # Fetch all records from tea.order.line.2

        # Group records by session ID
        session_records = defaultdict(list)
        for record in records:
            session_records[record.session_id].append(record)

        for session_id, items in session_records.items():
            # Initialize the items list for the session
            session_items = {  # Changed "PosSale" to "Items"
                "PropertyCode": "CCB1",
                "POSInterfaceCode": "CCB1-PS-20-000001",
                "ReceiptDate": items[0].ReceiptDate.isoformat(),
                "ReceiptTime": items[0].ReceiptTime,
                "ReceiptNo": items[0].ReceiptNo,
                "NoOfItems": len(items),
                "SalesCurrency": "LKR",
                "TotalSalesAmtB4Tax": items[0].TotalSalesAmtB4Tax,
                "TotalSalesAmtAfterTax": items[0].amount_total,
                # "SalesTaxRate": 5.00,
                "ServiceChargeAmt": 0.00,
                "PaymentAmt": 0.00,  # Initialize PaymentAmt to 0.00
                "PaymentCurrency": "LKR",
                "PaymentMethod": items[0].PaymentMethods,
                "SalesType": items[0].SalesType,
                "Items": [],
            }

            # Fetch payments for this session
            session_payments = payments.filtered(lambda p: p.session_id == session_id)
            for payment in session_payments:
                session_items['PaymentAmt'] += payment.PaymentAmt

            # Add items to the session_items dictionary
            for item in items:
                # Add item details to the Items list
                session_items['Items'].append({
                    "ItemDesc": item.full_product_name,
                    "ItemAmt": item.ItemAmt,
                })

            # Add session_items to the Items list in json_data
            json_data["Items"].append(session_items)  # Changed "PosSales" to "Items"

        # Convert JSON data to a string
        json_data_str = json.dumps(json_data, indent=4)

        # Raise UserError with the JSON data string
        raise exceptions.UserError(json_data_str)



    # def button_check(self):
    #     # Initialize the json_data dictionary
    #     json_data = {
    #         "AppCode": "POS-02",
    #         "PropertyCode": "CCB1",
    #         "ClientID": "CCB1-PS-20-000001",
    #         "ClientSecret": "S1D+qcjn47M=",
    #         "POSInterfaceCode": "CCB1-PS-20-000001",
    #         "BatchCode": "123",
    #         "PosSales": [],
    #     }

    #     # Fetch records from the current model
    #     records = self.env['tea.order.line'].search([])  # Fetch all records from tea.order.line
    #     payments = self.env['tea.order.line.2'].search([])  # Fetch all records from tea.order.line.2

    #     # Group records by session ID
    #     session_records = defaultdict(list)
    #     for record in records:
    #         session_records[record.session_id].append(record)

    #     for session_id, items in session_records.items():
    #         # Initialize the pos_sale dictionary for the session
    #         pos_sale = {
    #             "PropertyCode": "CCB1",
    #             "POSInterfaceCode": "CCB1-PS-20-000001",
    #             "ReceiptDate": items[0].ReceiptDate.isoformat(),
    #             # "ReceiptTime": "13:19:40",
    #             "ReceiptNo": items[0].ReceiptNo,
    #             # "NoOfItems": item[0].NoOfItems,
    #             "SalesCurrency": "LKR",
    #             # "TotalSalesAmtB4Tax": 500.00,
    #             "TotalSalesAmtAfterTax": items[0].amount_total,
    #             # "SalesTaxRate": 5.00,
    #             # "ServiceChargeAmt": 0.00,
    #             "PaymentAmt": 0.00,  # Initialize PaymentAmt to 0.00
    #             "PaymentCurrency": "LKR",
    #             "PaymentMethod": items[0].PaymentMethods,
    #             "SalesType": items[0].SalesType,
    #             "Items": [],
    #         }

    #         # Fetch payments for this session
    #         session_payments = payments.filtered(lambda p: p.session_id == session_id)
    #         for payment in session_payments:
    #             pos_sale['PaymentAmt'] += payment.PaymentAmt
    #             pos_sale['SalesType'] = payment.SalesType

    #         # Add items to the pos_sale dictionary
    #         for item in items:
    #             # Add item details to the Items list
    #             pos_sale['Items'].append({
    #                 "ItemDesc": item.full_product_name,
    #                 "ItemAmt": item.ItemAmt,
    #             })

    #         # Add pos_sale to the PosSales list in json_data
    #         json_data["PosSales"].append(pos_sale)

    #     # Convert JSON data to XML
    #     xml_data = dict_to_xml('Data', json_data)

    #     # Specify the directory where you want to save the XML file
    #     save_directory = "/Tea_Tang_Integration/data/"

    #     # Ensure the directory exists, if not create it
    #     if not os.path.exists(save_directory):
    #         os.makedirs(save_directory)

    #     # Write XML data to a file in the specified directory
    #     file_path = os.path.join(save_directory, 'output.xml')
    #     with open(file_path, 'w') as xml_file:
    #         xml_file.write(xml_data)






    # @api.model
    # def get_data_as_json(self):
    #     # Query the data
    #     records = self.search([])

    #     # Convert records into a list of dictionaries
    #     data_list = []
    #     for record in records:
    #         data_list.append({
    #             'custom_name': record.name,
    #             'ItemDesc': record.description,
    #             # Add more fields as needed
    #         })

    #     # Serialize the list of dictionaries into JSON format
    #     json_data = json.dumps(data_list)

    #     return json_data




