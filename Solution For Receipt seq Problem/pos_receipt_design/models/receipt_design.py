# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################
from odoo import api, fields, models, _

class ReceiptDesign(models.Model):
    _name = "receipt.design"
    _rec_name = "name"

    name = fields.Char(string="Name")
    receipt_design = fields.Text(string='Description', required=True)

    @api.model
    def _create_receipt_design_1(self):
        record_data = {}
        record_data['name'] = "Receipt Design 1"
        record_data['receipt_design'] = """ 
        <div class="pos-receipt">
            <div style="font-size: 80%; text-align:center;">
                <div><span t-esc='receipt.date.localestring'/>  <span t-esc='receipt.name'/></div>
            </div>
            <br/>
            <t t-if='receipt.company.logo'>
                <img style="width: 30%;display: block;margin: auto;" t-att-src='receipt.company.logo' alt="Logo"/>
                <br/>
            </t>
            <div style="font-size: 80%; text-align:center;">
                <t t-if='!receipt.company.logo'>
                    <h2 class="pos-receipt-center-align">
                        <t t-esc='receipt.company.name' />
                    </h2>
                </t>
                <t t-if='receipt.company.contact_address'>
                    <div><t t-esc='receipt.company.contact_address' /></div>
                </t>
                <t t-if='receipt.company.phone'>
                    <div>Tel:<t t-esc='receipt.company.phone' /></div>
                </t>
                <t t-if='receipt.company.website'>
                    <div><t t-esc='receipt.company.website' /></div>
                </t>
                <t t-if='receipt.header_html'>
                    <t t-raw='receipt.header_html' />
                </t>
                <t t-if='!receipt.header_html and receipt.header'>
                    <div><t t-esc='receipt.header' /></div>
                </t>
                <br/>
            </div>
            <br />
            <!-- Orderlines -->
            <div class='orderlines'>
                <div style="text-align:center; font-size: 75%; border-top: 1px dashed black;border-bottom: 1px dashed black;padding-top: 5px;padding-bottom: 5px;">
                    <div>Receipt : <span t-esc='receipt.name' /></div>
                    <br/>
                    <div>Date : 
                        <t t-if="order.formatted_validation_date">
                          <span t-esc='order.formatted_validation_date' />
                        </t>
                        <t t-else="">
                            <span t-esc='order.validation_date' />
                        </t>
                    </div>
                    <br/>
                    <t t-if='receipt.partner'>
                        <div>Client : <t t-esc='receipt.partner.name' /></div>
                        <br/>
                    </t>
                    <t t-if='receipt.cashier'>
                    <div class='cashier'>
                        <div>Served by <t t-esc='receipt.cashier' /></div>
                    </div>
                    </t>
                    
                    </div>
                    <br/>
                    <br/>
                    <table style="width: 100%;">
                        <tr style="border-bottom: 2px solid black;font-size:15px;">
                        <th style="text-align:left;">Product</th>
                        <th>Qty</th>
                        <th style="text-align: center;">Unit Price</th>
                        <th>Amount</th>
                        </tr>
                        <tr t-foreach="receipt.orderlines" t-as="line" t-key="line.id" style="border-bottom: 1px solid #ddd;font-size: 16px;font-family: initial;">
                        <td><div style="padding-top: 10px;padding-bottom: 10px;">
                            <span t-esc='line.productName'/>
                            <t  t-if="line.discount and line.discount !== '0'">
                                <h5 style="margin-top: 0%;margin-bottom: 0%;font-size: 12px;color: #848484;">
                                    <t t-esc='line.discount' />% Discount 
                                </h5>
                            </t>
                            <t t-if="line.customer_note">
                              <div style="font-size: 13px;" t-esc="line.customer_note"/>
                            </t>
                            </div>
                        </td>
                        <td style="text-align: center;"><span t-esc="line.qty"/><span t-if='line.unit !== "Units"' t-esc='line.unit'/></td>
                        <td style="text-align: center;"><span t-esc="line.unitPrice"/></td>
                        <td style="text-align: center;"><span t-esc='line.price'/></td>
                        </tr>
                    </table>
                </div>
          
 
            <!-- Subtotal -->
            <t t-set='taxincluded' t-value='Math.abs(receipt.total_without_tax - receipt.amount_total) &lt;= 0.000001' />
            <t t-if='!taxincluded'>
                <br/> 
                <div style="font-weight: 700;text-align: right; font-size: 20px;border-top: 2px solid;margin-left: 30%; padding-top: 2%;">Subtotal :
                <span t-esc='widget.utils.formatCurrency(receipt.total_without_tax)' class="pos-receipt-right-align"/></div>
                <t t-foreach='receipt.tax_details' t-as='tax' t-key='tax.name'>
                    <div style="font-weight: 700;text-align: right;">
                        <t t-esc='tax.name' />
                        <span t-esc='widget.utils.formatCurrency(tax.amount, false)' class="pos-receipt-right-align"/>
                    </div>
                </t>
            </t>
            <!-- Total -->
 
           
            <br/>
            <div style="font-size: 20px;text-align: right;font-weight: 700; border-top: 2px solid;margin-left: 30%;padding-top: 2%;">
                TOTAL :
                <span t-esc='widget.utils.formatCurrency(receipt.amount_total)'/>
            </div>
            <br/>
             <!--Extra Payment Info -->
             <t t-if='receipt.total_discount'>
                <div style="font-size: 14px;text-align: right;border-top: 1px solid;margin-left: 30%;padding-top: 2%;">
                    Discounts
                    <span t-esc='receipt.total_discount'/>
                </div>
            </t>
            <br/>
            <t t-if='taxincluded'>
                <t t-foreach='receipt.tax_details' t-as='tax' t-key='tax.tax.id'>
                    <div style="font-size: 15px; text-align: right; font-weight: 700; border-top: 1px solid;margin-left: 30%;padding-top: 2%;">
                        <t t-esc='tax.name' />
                        <span t-esc='widget.utils.formatCurrency(tax.amount, false)'/>
                    </div>
                </t>
                <div style="font-size: 15px; text-align: right; font-weight: 700;">
                    Total Taxes :
                    <span t-esc='widget.utils.formatCurrency(receipt.amount_tax)'/>
                </div>
            </t>
            </div>
            <br/>
            <br/>
            <div style="border-top: 1px dashed black;padding-top: 5%;border-bottom: 1px dashed black;">
                <!-- Payment Lines -->
                <t t-foreach='paymentlines' t-as='line' t-key='line.cid'>
                    <div class="paymentlines d-flex justify-content-between" style="font-size: 14px;">
                        <t t-esc='line.name' />
                        <span t-esc='widget.utils.formatCurrency(line.amount, false)' class="pos-receipt-right-align"/>
                    </div>
                </t>
                <br/>
                  <div class="d-flex justify-content-between pos-receipt-amount receipt-change mt-2 pos-receipt-amount receipt-change mt-2">
                    CHANGE
                    <span t-esc='widget.utils.formatCurrency(receipt.change)' class="pos-receipt-right-align"/>
                </div>
                <br/>
            </div>
           
           
           
            <div class='before-footer' />
            <!-- Footer -->
            <div t-if='receipt.footer_html'  class="pos-receipt-center-align" style="font-size: 14px;">
                <t t-raw='receipt.footer_html'/>
            </div>
            <div t-if='!receipt.footer_html and receipt.footer'  class="pos-receipt-center-align" style="font-size: 13px;">
                <br/>
                <t t-esc='receipt.footer'/>
                <br/>
                <br/>
            </div>
            <div class='after-footer' style="font-size: 14px;">
                <t t-foreach='paymentlines' t-as='line' t-key='line_index'>
                    <t t-if='line.ticket'>
                        <br />
                        <div class="pos-payment-terminal-receipt">
                            <t t-raw='line.ticket'/>
                        </div>
                    </t>
                </t>
            </div>
            <br/>
            <div style="text-align:center;">
                Thank You. Please Visit Again !!
            </div>
        </div>"""
        record_id = self.create(record_data)
        pos_config_id = self.env.ref('point_of_sale.pos_config_main')
        if record_id and pos_config_id:
            pos_config_id.use_custom_receipt = True
            pos_config_id.receipt_design_id = record_id.id

    @api.model
    def _create_receipt_design_2(self):
        record_data = {}
        record_data['name'] = "Receipt Design 2"
        record_data['receipt_design'] = """ 
        <div class="pos-receipt" style="font-family: monospace;">
            <div class="pos-center-align" style="font-size: 12px;">
                <t t-if="order.formatted_validation_date">
                    <t t-esc="order.formatted_validation_date"/>
                </t>
                <t t-else="">
                    <t t-esc="order.validation_date"/>
                </t> 
                <br/><t t-esc="order.name"/></div>
            <br />
            <t t-esc="widget.services.pos.company.name"/><br />
            <div style="font-size:13px">
                Phone: <t t-esc="widget.services.pos.company.phone || ''"/><br />
            </div>
            <div style="font-size:13px">
                User: <t t-esc="widget.services.pos.cashier ? widget.services.pos.cashier.name : widget.services.pos.user.name"/><br />
            </div>
            <br />
            <t t-if="receipt.header">
                <div style='text-align:center; font-size:13px'>
                    <t t-esc="receipt.header" />
                </div>
                <br />
            </t>
            <table class='receipt-orderlines' style="font-size:13px;">
                <colgroup>
                    <col width='45%' />
                    <col width='25%' />
                    <col width='30%' />
                </colgroup>
                <tr t-foreach="orderlines" t-as="orderline" t-key="orderline.id">
                    <td><div style="padding-top: 5px;padding-bottom: 5px;">
                          <t t-esc="orderline.get_product().display_name"/>
                           <t t-if="orderline.get_discount() > 0">
                              <div style="font-size: 12px;font-style: italic;color: #808080;">
                                  <t t-esc="orderline.get_discount()"/>% discount
                              </div>
                          </t>
                            <t t-if="orderline.customerNote">
                                <div style="font-size: 12px;" t-esc="orderline.customerNote"/>
                            </t>
                        </div>
                    </td>
                    <td class="pos-right-align">
                        <div>
                          <t t-esc="orderline.get_quantity_str_with_unit()"/>
                        </div>
                    </td>
                    <td class="pos-right-align">
                        <div>
                          <t t-esc="widget.utils.formatCurrency(orderline.get_display_price())"/>
                        </div>
                    </td>
                </tr>
            </table>
            <br />
            <!-- Subtotal -->
            <t t-set='taxincluded' t-value='Math.abs(receipt.total_without_tax - receipt.amount_total) &lt;= 0.000001' />
            <t t-if='!taxincluded'>
                <br/>
                <div style="font-weight: 700; font-size: 14px;">Subtotal<span t-esc='widget.utils.formatCurrency(receipt.total_without_tax)' class="pos-receipt-right-align"/></div>
                <t t-foreach='receipt.tax_details' t-as='tax' t-key='tax.id'>
                    <div style="font-weight: 700; font-size: 14px;">
                        <t t-esc='tax.name' />
                        <span t-esc='widget.utils.formatCurrency(tax.amount, false)' class="pos-receipt-right-align"/>
                    </div>
                </t>
            </t>
            <!-- Total -->
            <br/>
            <div style="font-weight: 700; font-size: 14px;">
                TOTAL
                <span t-esc='widget.utils.formatCurrency(receipt.amount_total)' class="pos-receipt-right-align"/>
            </div>
            <br/><br/>
            <!-- Payment Lines -->
            <t t-foreach='paymentlines' t-as='line' t-key='line.cid'>
                <div style="font-size: 14px;">
                    <t t-esc='line.name' />
                    <span t-esc='widget.utils.formatCurrency(line.amount, false)' class="pos-receipt-right-align"/>
                </div>
            </t>
            <br/>
            <div class="receipt-change" style="font-size: 14px;">
                CHANGE
                <span t-esc='widget.utils.formatCurrency(receipt.change)' class="pos-receipt-right-align"/>
            </div>
            <br/>
            <!-- Extra Payment Info -->
            <t t-if='receipt.total_discount'>
                <div style="font-size: 14px;">
                    Discounts
                    <span t-esc='widget.utils.formatCurrency(receipt.total_discount)' class="pos-receipt-right-align"/>
                </div>
            </t>
            <t t-if='taxincluded'>
                <t t-foreach='receipt.tax_details' t-as='tax' t-key='tax.tax.id'>
                    <div style="font-size: 14px;">
                        <t t-esc='tax.name' />
                        <span t-esc='widget.utils.formatCurrency(tax.amount, false)' class="pos-receipt-right-align"/>
                    </div>
                </t>
                <div style="font-size: 14px;">
                    Total Taxes
                    <span t-esc='widget.utils.formatCurrency(receipt.amount_tax)' class="pos-receipt-right-align"/>
                </div>
            </t>
            <div class='before-footer' />
            <!-- Footer -->
            <div t-if='receipt.footer_html' style="text-align: center; font-size: 14px;">
                <t t-raw='receipt.footer_html'/>
            </div>
            <div t-if='!receipt.footer_html and receipt.footer' style="text-align: center;font-size: 14px;">
                <br/>
                <t t-esc='receipt.footer'/>
                <br/><br/>
            </div>
            <div class='after-footer' style="font-size: 14px;">
                <t t-foreach='paymentlines' t-as='line' t-key='line_index'>
                    <t t-if='line.ticket'>
                        <br />
                        <div class="pos-payment-terminal-receipt">
                            <t t-raw='line.ticket'/>
                        </div>
                    </t>
                </t>
            </div>   
            <br/><br/>   
            <div style="text-align:center;border-top: 2px dotted black;padding-top: 15px;">
                <t t-if='receipt.cashier'>
                    <div class='cashier' style="text-align:center;">
                        <div>Served by <t t-esc='receipt.cashier' /></div>
                    </div>
                </t>
                <br/>
                Thank You. Please Visit Again !!
            </div>
        </div>"""
        self.create(record_data)

    @api.model
    def _create_receipt_design_3(self):
        record_data = {}
        record_data['name'] = "Receipt Design 3"
        record_data['receipt_design'] = """ 
        <div class="pos-receipt">
            <t t-esc="widget.services.pos.company.name"/><br />
            <div style="font-size:13px">
                Phone: <t t-esc="widget.services.pos.company.phone || ''"/><br />
            </div>
            <div style="font-size:13px">
                User : <t t-esc="widget.services.pos.cashier ? widget.services.pos.cashier.name : widget.services.pos.user.name"/><br />
            </div>
            <br/>
            <div style="font-size:13px">
                Date : 
                <t t-if="order.formatted_validation_date">
                    <t t-esc="order.formatted_validation_date"/>
                </t>
                <t t-else="">
                    <t t-esc="order.validation_date"/>
                </t>
                <br />
            </div>
            <div style="font-size:13px">
                Order : <t t-esc="order.name"/><br />
            </div>
            <br />
            <div style="font-size:13px">
                Cashier :  <t t-esc='receipt.cashier' /><br />
            </div>
            <br/>
            <t t-if="receipt.header">
                <div style='text-align:center; font-size:13px'>
                    <t t-esc="receipt.header" />
                </div>
                <br />
            </t>
            <div>
                <table class='receipt-orderlines' style="font-size:15px; border-style: double;
            border-left: none;border-right: none;border-bottom: none;width: 100%;">
                <colgroup>
                    <col width='40%' />
                    <col width='30%' />
                    <col width='30%' />
                </colgroup>
                <tr style="border-bottom: 1px dashed black;">
                    <th style="text-align:left;">Product</th>
                    <th style="text-align:center;">Qty</th>
                    <th style="text-align:center;">Amount</th>
                </tr>
                <tr t-foreach="orderlines" t-as="orderline" t-key='orderline.id'>
                    <td style="padding-top: 1%;padding-bottom: 1%;">
                        <t t-esc="orderline.get_product().display_name"/>
                        <t t-if="orderline.get_discount() > 0">
                            <div style="font-size: 12px;font-style: italic;color: #808080;">
                                <t t-esc="orderline.get_discount()"/>% discount
                            </div>
                        </t>
                        <t t-if="orderline.customerNote">
                            <div style="font-size: 14px;" t-esc="orderline.customerNote"/>
                        </t>
                    </td>
                    <td class="pos-center-align">
                        <t t-esc="orderline.get_quantity_str_with_unit()"/>
                    </td>
                    <td class="pos-center-align">
                        <t t-esc="widget.utils.formatCurrency(orderline.get_display_price())"/>
                    </td>
                </tr>
                </table>
            </div>
            <br />
            <div style="padding-top: 6px;">
                <!-- Subtotal -->
                <t t-set='taxincluded' t-value='Math.abs(receipt.total_without_tax - receipt.amount_total) &lt;= 0.000001' />
                <t t-if='!taxincluded'>
                    <br/>
                    <div style="font-weight: 700; font-size: 14px; border-top:1px dashed;"><span style="margin-left: 40%;">Subtotal : </span>
                    <span t-esc='widget.utils.formatCurrency(receipt.total_without_tax)' class="pos-receipt-right-align"/></div>
                    <t t-foreach='receipt.tax_details' t-as='tax' t-key='tax.name'>
                        <div style="font-weight: 700; font-size: 14px;">
                            <span style="margin-left: 40%;"><t t-esc='tax.name' /></span>
                            <span t-esc='widget.utils.formatCurrency(tax.amount, false)' class="pos-receipt-right-align"/>
                        </div>
                    </t>
                </t>
                <!-- Total -->
                <br/>
                <div style="font-weight: 700; font-size: 14px;">
                    <span style="margin-left: 40%;">TOTAL : </span>
                    <span t-esc='widget.utils.formatCurrency(receipt.amount_total)' class="pos-receipt-right-align"/>
                </div>
                <br/><br/>
            </div>
            <!-- Payment Lines -->
            <t t-foreach='paymentlines' t-as='line' t-key='line.cid'>
                <div style="font-size: 14px;border-top:1px dashed;padding-top: 5px;">
                    <span style="margin-left: 40%;"><t t-esc='line.name' /></span>
                    <span t-esc='widget.utils.formatCurrency(line.amount, false)' class="pos-receipt-right-align"/>
                </div>
            </t>
            <br/>  
            <div class="receipt-change" style="font-size: 14px;">
            <span style="margin-left: 40%;">CHANGE : </span>
                <span t-esc='widget.utils.formatCurrency(receipt.change)' class="pos-receipt-right-align"/>
            </div>
            <br/>
            <!-- Extra Payment Info -->
            <t t-if='receipt.total_discount'>
                <div style="font-size: 14px; border-top:1px dashed;padding-top: 5px;">
                    <span style="margin-left: 40%;">Discounts : </span>
                    <span t-esc='widget.utils.formatCurrency(receipt.total_discount)' class="pos-receipt-right-align"/>
                </div>
            </t>
            <t t-if='taxincluded'>
                <t t-foreach='receipt.tax_details' t-as='tax' t-key='tax.tax.id'>
                    <div style="font-size: 14px;">
                        <span style="margin-left: 40%;"><t t-esc='tax.name' /></span>
                        <span t-esc='widget.utils.formatCurrency(tax.amount, false)' class="pos-receipt-right-align"/>
                    </div>
                </t>
                <div style="font-size: 14px;">
                    <span style="margin-left: 40%;">Total Taxes : </span>
                    <span t-esc='widget.utils.formatCurrency(receipt.amount_tax)' class="pos-receipt-right-align"/>
                </div>
            </t>
            <div class='before-footer' />
            <!-- Footer -->
            <div t-if='receipt.footer_html' style="text-align: center; font-size: 14px;">
                <t t-raw='receipt.footer_html'/>
            </div>
            <div t-if='!receipt.footer_html and receipt.footer' style="text-align: center;font-size: 14px;">
                <br/>
                <t t-esc='receipt.footer'/>
                <br/><br/>
            </div>
            <div class='after-footer' style="font-size: 14px;">
                <t t-foreach='paymentlines' t-as='line' t-key='line_index'>
                    <t t-if='line.ticket'>
                        <br />
                        <div class="pos-payment-terminal-receipt">
                            <t t-raw='line.ticket'/>
                        </div>
                    </t>
                </t>
            </div>
            <br/><br/>
            <div>
                Thank You. Please Visit Again !!
            </div>
        </div>"""
        self.create(record_data)

    @api.model
    def _create_receipt_design_4(self):
        record_data = {}
        record_data['name'] = "Receipt Design 4"
        record_data['receipt_design'] = """
        <div class="pos-receipt" style="font-family: 'Inconsolata';">
            <div class="pos-receipt-order-data" style="font-size: 14px;">
                <t t-if="order.formatted_validation_date">
                    <t t-esc="order.formatted_validation_date"/>
                </t>
                <t t-else="">
                    <t t-esc="order.validation_date"/>
                </t> 
                <t t-esc="order.name"/></div>
            <br />
            <div class="pos-receipt-contact" style="font-size: 14px; font-family: 'Inconsolata'; text-align:left;">
                <div style="font-size:15px;">
                <t t-esc="widget.services.pos.company.name"/><br />
                </div>
                <div>
                    Phone: <t t-esc="widget.services.pos.company.phone || ''"/><br />
                </div>
                <div class='cashier'>
                    User: <t t-esc="widget.services.pos.cashier ? widget.services.pos.cashier.name : widget.services.pos.user.name"/><br />
                </div>
                <br />
                <t t-if="receipt.header">
                    <div style='text-align:center;'>
                        <t t-esc="receipt.header" />
                    </div>
                    <br />
                </t>
            </div>
            <table class='orderlines'>
                <colgroup>
                    <col width='40%' />
                    <col width='30%' />
                    <col width='30%' />
                </colgroup>
                <tr t-foreach="orderlines" t-as="orderline" t-key='orderline.id'>
                    <td><div style="padding-top: 5px;padding-bottom: 5px;">
                        <t t-esc="orderline.get_product().display_name"/>
                        <t t-if="orderline.get_discount() > 0">
                            <div style="font-size: 12px;font-style: italic;color: #808080;">
                                <t t-esc="orderline.get_discount()"/>% discount
                            </div>
                        </t>
                        <t t-if="orderline.customerNote">
                            <div style="font-size: 14px;" t-esc="orderline.customerNote"/>
                        </t>
                        </div>
                    </td>
                    <td style="text-align:right;">
                        <div>
                        <t t-esc="orderline.get_quantity_str_with_unit()"/>
                        </div>
                    </td>
                    <td style="text-align:right;">
                        <div>
                        <t t-esc="widget.utils.formatCurrency(orderline.get_display_price())"/>
                        </div>
                    </td>
                </tr>
            </table>
            <br />
            <table style="width: 100%;">
                <tr>
                    <td>Subtotal:</td>
                    <td class="pos-receipt-right-align">
                        <t t-esc="widget.utils.formatCurrency(order.get_total_without_tax())"/>
                    </td>
                </tr>
                <t t-foreach="order.get_tax_details()" t-as="taxdetail" t-key='taxdetail.name'>
                    <tr>
                        <td><t t-esc="taxdetail.name" /></td>
                        <td class="pos-receipt-right-align">
                            <t t-esc="widget.utils.formatCurrency(taxdetail.amount)" />
                        </td>
                    </tr>
                </t>
                <tr>
                    <t t-if="order.get_total_discount() > 0">
                        <td>Discount:</td>
                        <td class="pos-receipt-right-align">
                            <t t-esc="widget.utils.formatCurrency(order.get_total_discount())"/>
                        </td>
                    </t>
                </tr>
                <tr style="font-size: 20px;margin: 5px;">
                    <td>Total:</td>
                    <td class="pos-receipt-right-align">
                        <t t-esc="widget.utils.formatCurrency(order.get_total_with_tax())"/>
                    </td>
                </tr>
            </table>
            <br />
            <table style="width: 100%;">
                <t t-foreach="paymentlines" t-as="line" t-key='line.cid'>
                    <tr>
                        <td>
                            <t t-esc="line.name"/>
                        </td>
                        <td class="pos-receipt-right-align">
                            <t t-esc="widget.utils.formatCurrency(line.get_amount())"/>
                        </td>
                    </tr>
                </t>
            </table>
            <br />
            <table style="width: 100%;">
                <tr><td>Change:</td><td class="pos-receipt-right-align">
                    <t t-esc="widget.utils.formatCurrency(order.get_change())"/>
                    </td></tr>
            </table>
            <t t-if="receipt.footer">
                <br />
                <div style='text-align:center'>
                    <t t-esc="receipt.footer" />
                </div>
            </t>
        </div>"""
        self.create(record_data)
        
class PosSession(models.Model):
    _inherit = "pos.session"
    
    def _loader_params_receipt_design(self):
        return {'search_params': {'fields': []}}
    
    def _pos_ui_models_to_load(self):
        models = super()._pos_ui_models_to_load()
        if 'receipt.design' not in models:
            models.append('receipt.design')
        return models
    
    def _get_pos_ui_receipt_design(self, params):
        receipt_design = self.env['receipt.design'].search_read(**params['search_params'])
        return receipt_design
