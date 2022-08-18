# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    purchase_price_subtotal = fields.Float(
        string='Cost', compute="_compute_purchase_price_subtotal",
        digits='Product Price', store=True, readonly=False,
        groups="base.group_user")

    @api.depends("purchase_price", "product_uom_qty")
    def _compute_purchase_price_subtotal(self):
        for line in self:
            line.purchase_price_subtotal = line.purchase_price * line.product_uom_qty

    @api.depends('price_subtotal', 'product_uom_qty', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            line.margin = line.price_subtotal - (line.purchase_price * line.product_uom_qty)
            line.margin_percent = (line.purchase_price * line.product_uom_qty) and line.margin / (
                    line.purchase_price * line.product_uom_qty)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.margin', 'amount_untaxed')
    def _compute_margin(self):
        if not all(self._ids):
            for order in self:
                order.margin = sum(order.order_line.mapped('margin'))

                order.margin_percent = sum(order.order_line.mapped('purchase_price_subtotal')) and order.margin / sum(
                    order.order_line.mapped('purchase_price_subtotal'))
        else:
            self.env["sale.order.line"].flush(['margin'])
            # On batch records recomputation (e.g. at install), compute the margins
            # with a single read_group query for better performance.
            # This isn't done in an onchange environment because (part of) the data
            # may not be stored in database (new records or unsaved modifications).
            grouped_order_lines_data = self.env['sale.order.line'].read_group(
                [
                    ('order_id', 'in', self.ids),
                ], ['margin', 'order_id'], ['order_id'])
            mapped_data = {m['order_id'][0]: m['margin'] for m in grouped_order_lines_data}
            for order in self:
                order.margin = mapped_data.get(order.id, 0.0)
                order.margin_percent = sum(order.order_line.mapped('purchase_price_subtotal')) and order.margin / sum(
                    order.order_line.mapped('purchase_price_subtotal'))

    def update_all_margin(self):
        if not all(self._ids):
            for line in self.env["sale.order"].search([]):
                for record in line.order_line:
                    record.margin = record.price_subtotal - (record.purchase_price * record.product_uom_qty)
                    record.margin_percent = (record.purchase_price * record.product_uom_qty) and record.margin / (
                            record.purchase_price * record.product_uom_qty)
                line.margin = sum(line.order_line.mapped('margin'))

                line.margin_percent = sum(line.order_line.mapped('purchase_price_subtotal')) and line.margin / sum(
                    line.order_line.mapped('purchase_price_subtotal'))
        else:
            self.env["sale.order.line"].flush(['margin'])
            # On batch records recomputation (e.g. at install), compute the margins
            # with a single read_group query for better performance.
            # This isn't done in an onchange environment because (part of) the data
            # may not be stored in database (new records or unsaved modifications).
            grouped_order_lines_data = self.env['sale.order.line'].read_group(
                [
                    ('order_id', 'in', self.ids),
                ], ['margin', 'order_id'], ['order_id'])
            mapped_data = {m['order_id'][0]: m['margin'] for m in grouped_order_lines_data}
            for order in self:
                for record in order.order_line:
                    record.margin = record.price_subtotal - (record.purchase_price * record.product_uom_qty)
                    record.margin_percent = (record.purchase_price * record.product_uom_qty) and record.margin / (
                            record.purchase_price * record.product_uom_qty)
                order.margin = mapped_data.get(order.id, 0.0)
                order.margin_percent = sum(order.order_line.mapped('purchase_price_subtotal')) and order.margin / sum(
                    order.order_line.mapped('purchase_price_subtotal'))
