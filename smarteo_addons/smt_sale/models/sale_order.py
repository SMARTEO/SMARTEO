# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    _description = "Sale Order Line"

    purchase_price_subtotal = fields.Float(
        string="Cost",
        compute="_compute_purchase_price_subtotal",
        digits="Product Price",
        store=True,
        readonly=False,
        groups="base.group_user",
    )
    is_set_desc_lines = fields.Boolean(compute="_compute_is_set_desc_lines")

    @api.depends("display_type")
    def _compute_is_set_desc_lines(self):
        can_edit = self.env.user.has_group("smt_sale.is_set_desc_lines_security")
        for line in self:
            line.is_set_desc_lines = can_edit or line.display_type in ("line_section", "line_note")

    @api.depends("purchase_price", "product_uom_qty")
    def _compute_purchase_price_subtotal(self):
        for line in self:
            line.purchase_price_subtotal = line.purchase_price * line.product_uom_qty

    @api.depends("price_subtotal", "product_uom_qty", "purchase_price")
    def _compute_margin(self):
        for line in self:
            line.margin = line.price_subtotal - (line.purchase_price * line.product_uom_qty)
            cost = line.purchase_price * line.product_uom_qty
            line.margin_percent = line.margin / cost if cost else 0


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Sale Order"

    def action_open_crm(self):
        self.ensure_one()
        crm_id = self.opportunity_id
        action = self.env["ir.actions.actions"]._for_xml_id("crm.crm_lead_action_pipeline")
        if len(crm_id) > 1:
            action["domain"] = [("id", "in", crm_id.ids)]
        elif len(crm_id) == 1:
            form_view = [(self.env.ref("crm.crm_lead_view_form").id, "form")]
            if "views" in action:
                action["views"] = form_view + [
                    (state, view) for state, view in action["views"] if view != "form"
                ]
            else:
                action["views"] = form_view
            action["res_id"] = crm_id.ids[0]
        else:
            action = {"type": "ir.actions.act_window_close"}
        action["context"] = dict(self._context, create=False)
        return action

    @api.depends("order_line.margin", "amount_untaxed")
    def _compute_margin(self):
        if not all(self._ids):
            for order in self:
                order.margin = sum(order.order_line.mapped("margin"))
                cost = sum(order.order_line.mapped("purchase_price_subtotal"))
                order.margin_percent = order.margin / cost if cost else 0
        else:
            self.env["sale.order.line"].flush_model(["margin"])
            grouped = self.env["sale.order.line"]._read_group(
                [("order_id", "in", self.ids)],
                groupby=["order_id"],
                aggregates=["margin:sum"],
            )
            mapped_data = {order.id: margin_sum for order, margin_sum in grouped}
            for order in self:
                order.margin = mapped_data.get(order.id, 0.0)
                cost = sum(order.order_line.mapped("purchase_price_subtotal"))
                order.margin_percent = order.margin / cost if cost else 0

    def update_all_margin(self):
        # Deliberately unbounded: this recomputes margins for every order in
        # the database, not a filtered subset.
        for order in self.env["sale.order"].search([]):  # pylint: disable=no-search-all
            for line in order.order_line:
                cost = line.purchase_price * line.product_uom_qty
                line.margin = line.price_subtotal - cost
                line.margin_percent = line.margin / cost if cost else 0
            order.margin = sum(order.order_line.mapped("margin"))
            cost = sum(order.order_line.mapped("purchase_price_subtotal"))
            order.margin_percent = order.margin / cost if cost else 0
