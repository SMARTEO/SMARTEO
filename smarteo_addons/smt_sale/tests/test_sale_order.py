# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderActionOpenCrm(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "CRM Sale Partner"})

    def test_action_open_crm_with_one_opportunity(self):
        lead = self.env["crm.lead"].create(
            {
                "name": "Linked Opportunity",
                "type": "opportunity",
                "partner_id": self.partner.id,
            }
        )
        order = self.env["sale.order"].create(
            {"partner_id": self.partner.id, "opportunity_id": lead.id}
        )

        action = order.action_open_crm()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_id"], lead.id)
        self.assertEqual(action["views"][0], (self.env.ref("crm.crm_lead_view_form").id, "form"))

    def test_action_open_crm_without_opportunity_closes_window(self):
        order = self.env["sale.order"].create({"partner_id": self.partner.id})

        action = order.action_open_crm()

        self.assertEqual(
            action, {"type": "ir.actions.act_window_close", "context": action["context"]}
        )


@tagged("post_install", "-at_install")
class TestSaleOrderMargin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Margin Test Partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Margin Test Product",
                "type": "consu",
                "list_price": 100.0,
                "standard_price": 40.0,
            }
        )

    def _create_order_with_line(self):
        order = self.env["sale.order"].create({"partner_id": self.partner.id})
        self.env["sale.order.line"].create(
            {
                "order_id": order.id,
                "product_id": self.product.id,
                "product_uom_qty": 2,
                "price_unit": 100.0,
                "purchase_price": 40.0,
            }
        )
        return order

    def test_order_margin_aggregates_line_margins(self):
        order = self._create_order_with_line()

        order._compute_margin()

        self.assertEqual(order.margin, 120.0)
        self.assertEqual(order.margin_percent, 1.5)

    def test_update_all_margin_recomputes_margin_fields(self):
        order = self._create_order_with_line()
        order.order_line.margin = 0.0
        order.margin = 0.0

        self.env["sale.order"].update_all_margin()

        self.assertEqual(order.order_line.margin, 120.0)
        self.assertEqual(order.margin, 120.0)
