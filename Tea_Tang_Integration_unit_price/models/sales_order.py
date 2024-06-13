from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
<<<<<<< HEAD
    partner_ref = fields.Char(string="Partner Ref", related='order_id.partner_ref', store=True)
=======

#     new_field = fields.Integer(string="My Field", store=True)
#     name_lbx = fields.Char(string="Name Lbx", related='order_id.name', store=True)
    partner_ref = fields.Char(string="Partner Ref", related='order_id.partner_ref', store=True)

#     new_field_connect = fields.Many2one('sale.order.line', string="Related Sale Order Line")

#     price_unit = fields.Float(
#         string='Unit Price', required=True, digits='Product Price',
#         compute="_compute_price_unit_new_data", readonly=False, store=True)
    


#     @api.depends('partner_ref')
#     def _compute_price_unit_new_data(self):
#         for record in self:
#             # Search for the sale order line with matching partner reference
#             valuation_layer = self.env['sale.order.line'].search([('name_lbx', '=', record.partner_ref)], limit=1)
            
#             # Check if a matching sale order line was found
#             if valuation_layer:
#                 record.price_unit = valuation_layer.price_unit
#             else:
#                 record.price_unit = 0.00
>>>>>>> 7058ea7cfbf89ab97209f65e017e433d04d557a1


#     # @api.depends('partner_ref', 'new_field_connect.price_unit')
#     def compute_price_unit_new(self):
#         for record in self:
#             if record.partner_ref:
#                 raise UserError(record.partner_ref)
#             # if record.partner_ref and record.new_field_connect.name_lbx:

#             #     record.price_unit = record.new_field_connect.price_unit
#             # else:
#             #     record.price_unit = 0.0

    def compute_price_unit_new_test(self):
        for record in self:
            if not record.partner_ref:
                raise UserError("There is no partner ref")
            
            # Search for the stock move with matching partner reference
            valuation_layer = self.env['stock.move'].search([('form_po', '=', record.order_id.id)], limit=1)
            
            # Check if a matching stock move was found
            if valuation_layer:
                # Raise a UserError with the id of the matching stock move
                raise UserError(f"The matching stock move ID is: {valuation_layer.cost_per_unit}")
            else:
                # Handle the case where no matching stock move was found
                raise UserError("No matching stock move found for the given partner reference.")

    
                    


class Picking(models.Model):
    _inherit = "stock.picking"


    # name_lbx = fields.Char(string="Name Lbx", related='picking_id.name', store=True)
    

    # def button_update_valuation_layer_value(self):
    #     for picking in self:
    #         for move in picking.move_ids_without_package:
    #             if move.id:
    #                 valuation_layer = self.env['stock.valuation.layer'].search([('stock_move_id', '=', move.id)], limit=1)
    #                 if valuation_layer:
    #                     move.valuation_layer_value = abs(valuation_layer.value)

    # def button_update_valuation_layer_value(self):
    #     for picking in self:
    #         for move in picking.move_ids_without_package:
    #             if move.id:
    #                 # Search for the stock valuation layer with matching stock move ID
    #                 valuation_layer = self.env['stock.valuation.layer'].search([('stock_move_id', '=', move.id)], limit=1)
                    
    #                 # Search for the purchase order line with matching partner reference
    #                 valuation_layer_02 = self.env['purchase.order.line'].search([('partner_ref', '=', move.reference_ne_ms)], limit=1)
                    
    #                 # Update the valuation_layer_value field in stock move
    #                 if valuation_layer:
    #                     move.valuation_layer_value = abs(valuation_layer.value)
                    
    #                 # Update the from_po field in stock move
    #                 if valuation_layer_02:
    #                     move.form_po = valuation_layer_02.order_id


    # This code is working But There is a issu to check that is that working or is that changing the price unit as for product and confirm the code
    def button_update_valuation_layer_value(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                if move.id:
                    # Search for the stock valuation layer with matching stock move ID
                    valuation_layer = self.env['stock.valuation.layer'].search([('stock_move_id', '=', move.id)], limit=1)
                    
                    # Search for all purchase order lines with matching partner reference
                    purchase_order_lines = self.env['purchase.order.line'].search([('partner_ref', '=', move.reference_ne_ms)])
                    
                    # Update the valuation_layer_value field in stock move
                    if valuation_layer:
                        move.valuation_layer_value = abs(valuation_layer.value)
                    
                    # Iterate over each purchase order line and update the price unit
                    for purchase_order_line in purchase_order_lines:
                        # Update the from_po field in stock move if it matches
                        if purchase_order_line:
                            move.form_po = purchase_order_line.order_id.id

                            # Check if the purchase order line has an order_id and matches the stock move's form_po
                            if purchase_order_line.order_id.id == move.form_po and purchase_order_line.product_id == move.product_id:
                                # Update the price_unit in purchase order line using stock move's cost_per_unit
                                purchase_order_line.price_unit = move.cost_per_unit



class StockMove(models.Model):
    _inherit = "stock.move"

    valuation_layer_value = fields.Float("Total Cost")
    cost_per_unit = fields.Float("Cost Per Unit", compute='_compute_cost_per_unit', store=True)
    reference_ne_ms = fields.Char(string="Partner Ref", related='picking_id.origin', store=True)
    form_po = fields.Integer(string="Order ID", store=True)

    @api.depends('valuation_layer_value', 'quantity')
    def _compute_cost_per_unit(self):
        for record in self:
            if record.valuation_layer_value and record.quantity:
                record.cost_per_unit = record.valuation_layer_value / record.quantity
            else:
                record.cost_per_unit = 0.0


class Picking(models.Model):
    _inherit = "stock.picking"

    # This code is working But There is a issu to check that is that working or is that changing the price unit as for product and confirm the
    def button_update_valuation_layer_value(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                if move.id:
                    # Search for the stock valuation layer with matching stock move ID
                    valuation_layer = self.env['stock.valuation.layer'].search([('stock_move_id', '=', move.id)], limit=1)
                    
                    # Search for all purchase order lines with matching partner reference
                    purchase_order_lines = self.env['purchase.order.line'].search([('partner_ref', '=', move.reference_ne_ms)])
                    
                    # Update the valuation_layer_value field in stock move
                    if valuation_layer:
                        move.valuation_layer_value = abs(valuation_layer.value)
                    
                    # Iterate over each purchase order line and update the price unit
                    for purchase_order_line in purchase_order_lines:
                        # Update the from_po field in stock move if it matches
                        if purchase_order_line:
                            move.form_po = purchase_order_line.order_id.id

                            # Check if the purchase order line has an order_id and matches the stock move's form_po
                            if purchase_order_line.order_id.id == move.form_po and purchase_order_line.product_id == move.product_id:
                                # Update the price_unit in purchase order line using stock move's cost_per_unit
                                purchase_order_line.price_unit = move.cost_per_unit



class StockMove(models.Model):
    _inherit = "stock.move"

    valuation_layer_value = fields.Float("Total Cost")
    cost_per_unit = fields.Float("Cost Per Unit", compute='_compute_cost_per_unit', store=True)
    reference_ne_ms = fields.Char(string="Partner Ref", related='picking_id.origin', store=True)
    form_po = fields.Integer(string="Order ID", store=True)

    @api.depends('valuation_layer_value', 'quantity')
    def _compute_cost_per_unit(self):
        for record in self:
            if record.valuation_layer_value and record.quantity:
                record.cost_per_unit = record.valuation_layer_value / record.quantity
            else:
                record.cost_per_unit = 0.0


<<<<<<< HEAD

=======
    # sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    # def unit_confirm(self):
    #     raise UserError("Hello")
        # purchase_order_lines = self.env['purchase.order.line'].search([])
        # sale_order_lines = self.env['sale.order.line'].search([])

        # for purchase_order_line in purchase_order_lines:
        #     sale_order_lines_matched = sale_order_lines.filtered(lambda l: l.client_order_ref == purchase_order_line.name_lbx and l.product_id.id == purchase_order_line.product_id.id and l.name_lbx == purchase_order_line.partner_ref)
        #     for sale_order_line_matched in sale_order_lines_matched:
        #         purchase_order_line.write({'price_unit': sale_order_line_matched.price_unit})


    def unit_confirm(self):
        for purchase_order in self:
            for purchase_order_line in purchase_order.order_line:  # Loop through order lines of the related purchase order
                # Search for the stock move with matching purchase_order_id
                valuation_layer = self.env['stock.move'].search([('form_po', '=', purchase_order.id)], limit=1)
        
                # Update the unit_price field in purchase order line
                if valuation_layer:
                    old_price = purchase_order_line.price_unit
                    new_price = valuation_layer.cost_per_unit
                    purchase_order_line.price_unit = new_price
                    # _logger.info(f"Updated purchase order line {purchase_order_line.id}: price_unit from {old_price} to {new_price}")


    # def unit_confirm(self):
    #     for purchase_order in self:
    #         for purchase_order_line in purchase_order.order_line:
    #             # Debugging: Check if partner_ref is available
    #             # if not purchase_order_line.partner_ref:
    #             #     raise UserError(f"No partner_ref for Purchase Order Line ID: {purchase_order_line.id}")
                
    #             # if purchase_order_line.partner_ref:
    #             #     raise UserError(f"No partner_ref for Purchase Order Line ID: {purchase_order_line.partner_ref}")
                
                
    #             domain = [
    #                 # ('product_id', '=', purchase_order_line.product_id.id),
    #                 ('reference_ne_ms', '=', purchase_order_line.partner_ref)
    #                 # (TTPL00054, '=', purchase_order_line.partner_ref)
    #             ]
                
    #             # Search for the sale order line with a matching partner reference and product_id
    #             valuation_layer = self.env['stock.move'].search(domain, limit=1)

    #             if valuation_layer:
    #                 raise UserError(f"valuation_layer partner_ref: {valuation_layer.origin},{valuation_layer.reference_ne_ms},{valuation_layer.product_id.name},{valuation_layer.id}")
                
                
    #             if valuation_layer:
    #                 raise UserError(f"cost_per_unit: {valuation_layer.id}")
    #                 # purchase_order_line.price_unit = valuation_layer.cost_per_unit
    #             else:
    #                 raise UserError("Im shahidh")
                
                # For debugging purposes
                # raise UserError(f"Purchase Order Line ID: {purchase_order_line.id}, Product ID: {purchase_order_line.product_id.id}, Partner Ref: {purchase_order_line.partner_ref}, Price Unit: {purchase_order_line.price_unit}")

    # def unit_confirm(self):
    #     # Iterate through each purchase order line in the purchase order
    #     for purchase_order in self:
    #         for purchase_order_line in purchase_order.order_line:
    #             # Use the IDs of the relational objects for the domain filter
    #             domain = [
    #                 ('product_id', '=', purchase_order_line.product_id.id),
    #                 ('partner_ref','=',purchase_order_line.partner_ref)
    #             ]
                
    #             # Search for the sale order line with a matching partner reference and product_id
    #             valuation_layer = self.env['stock.move'].search(domain, limit=1)
                
    #             # Check if a matching sale order line was found
    #             if valuation_layer:
    #                 # Update the price_unit of the purchase order line
    #                 purchase_order_line.price_unit = valuation_layer.cost_per_unit
    #             else:
    #                 # If no matching sale order line is found, set price_unit to 0.00 or handle it as needed
    #                 purchase_order_line.price_unit = 0.00

                # If you need to raise an error for testing purposes, uncomment the next line
                # raise UserError(f"Purchase Order Line {purchase_order_line.id}: Unit price set to {purchase_order_line.price_unit}")
>>>>>>> 7058ea7cfbf89ab97209f65e017e433d04d557a1


# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"

<<<<<<< HEAD
=======
    # new_field = fields.Many2one('purchase.order.line', string="Related Purchase Order Line")

    # price_unit = fields.Float(
    #     string="Unit Price",
    #     compute='_compute_price_unit_new',
    #     digits='Product Price',
    #     store=True, readonly=False, required=True, precompute=True)
    
    # @api.depends('name_lbx', 'new_field')
    # def _compute_price_unit_new(self):
    #     for record in self:
    #         if record.name_lbx and record.new_field:
    #             record.price_unit = record.new_field.price_unit
    #         else:
    #             record.price_unit = 0.0

    # client_order_ref = fields.Char(string="Client Order Ref", related='order_id.client_order_ref', store=True)
    # name_lbx = fields.Char(string="Name Lbx", related='order_id.name', store=True)
>>>>>>> 7058ea7cfbf89ab97209f65e017e433d04d557a1
