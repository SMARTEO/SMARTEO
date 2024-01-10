# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    purchase_price_subtotal = fields.Float(
        string='Cost', compute="_compute_purchase_price_subtotal",
        digits='Product Price', store=True, readonly=False,
        groups="base.group_user")
    is_set_desc_lines = fields.Boolean(compute='_is_set_des_lines')

    @api.depends('display_type')
    def _is_set_des_lines(self):
        can_edit = self.env.user.has_group('smt_sale.is_set_desc_lines_security')
        for line in self:
            line.is_set_desc_lines = can_edit or line.display_type in ('line_section', 'line_note')

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

    def action_open_crm(self):
        self.ensure_one()
        crm_id = self.opportunity_id
        action = self.env["ir.actions.actions"]._for_xml_id("crm.crm_lead_action_pipeline")
        if len(crm_id) > 1:
            action['domain'] = [('id', 'in', crm_id.ids)]
        elif len(crm_id) == 1:
            form_view = [(self.env.ref('crm.crm_lead_view_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = crm_id.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        action['context'] = dict(self._context, create=False)
        return action

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
        # if not all(self._ids):
        for line in self.env["sale.order"].search([]):
            for record in line.order_line:
                record.margin = record.price_subtotal - (record.purchase_price * record.product_uom_qty)
                record.margin_percent = (record.purchase_price * record.product_uom_qty) and record.margin / (
                        record.purchase_price * record.product_uom_qty)
            line.margin = sum(line.order_line.mapped('margin'))

            line.margin_percent = sum(line.order_line.mapped('purchase_price_subtotal')) and line.margin / sum(
                line.order_line.mapped('purchase_price_subtotal'))
        # else:
        #     self.env["sale.order.line"].flush(['margin'])
        #     # On batch records recomputation (e.g. at install), compute the margins
        #     # with a single read_group query for better performance.
        #     # This isn't done in an onchange environment because (part of) the data
        #     # may not be stored in database (new records or unsaved modifications).
        #     grouped_order_lines_data = self.env['sale.order.line'].read_group(
        #         [
        #             ('order_id', 'in', self.ids),
        #         ], ['margin', 'order_id'], ['order_id'])
        #     mapped_data = {m['order_id'][0]: m['margin'] for m in grouped_order_lines_data}
        #     for order in self:
        #         for record in order.order_line:
        #             record.margin = record.price_subtotal - (record.purchase_price * record.product_uom_qty)
        #             record.margin_percent = (record.purchase_price * record.product_uom_qty) and record.margin / (
        #                     record.purchase_price * record.product_uom_qty)
        #         order.margin = mapped_data.get(order.id, 0.0)
        #         order.margin_percent = sum(order.order_line.mapped('purchase_price_subtotal')) and order.margin / sum(
        #             order.order_line.mapped('purchase_price_subtotal'))
