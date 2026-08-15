# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderLineMargin(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Sale Line Test Partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Sale Line Test Product",
                "type": "consu",
                "list_price": 100.0,
                "standard_price": 40.0,
            }
        )
        cls.order = cls.env["sale.order"].create({"partner_id": cls.partner.id})

    def _create_line(self, **extra_vals):
        vals = {
            "order_id": self.order.id,
            "product_id": self.product.id,
            "product_uom_qty": 2,
            "price_unit": 100.0,
            "purchase_price": 40.0,
        }
        vals.update(extra_vals)
        return self.env["sale.order.line"].create(vals)

    def test_purchase_price_subtotal(self):
        line = self._create_line()

        self.assertEqual(line.purchase_price_subtotal, 80.0)

    def test_purchase_price_subtotal_updates_with_quantity(self):
        line = self._create_line()

        line.product_uom_qty = 5

        self.assertEqual(line.purchase_price_subtotal, 200.0)

    def test_margin_and_margin_percent(self):
        line = self._create_line()

        line._compute_margin()

        self.assertEqual(line.margin, 120.0)
        self.assertEqual(line.margin_percent, 1.5)

    def test_margin_percent_zero_when_no_cost(self):
        line = self._create_line(purchase_price=0.0)

        line._compute_margin()

        self.assertEqual(line.margin_percent, 0.0)

    def test_is_set_desc_lines_false_for_regular_product_line(self):
        line = self._create_line()

        line._compute_is_set_desc_lines()

        self.assertFalse(line.is_set_desc_lines)

    def test_is_set_desc_lines_true_for_section_line(self):
        section_line = self.env["sale.order.line"].create(
            {
                "order_id": self.order.id,
                "display_type": "line_section",
                "name": "A Section",
            }
        )

        section_line._compute_is_set_desc_lines()

        self.assertTrue(section_line.is_set_desc_lines)

    def test_is_set_desc_lines_true_for_note_line(self):
        note_line = self.env["sale.order.line"].create(
            {
                "order_id": self.order.id,
                "display_type": "line_note",
                "name": "A Note",
            }
        )

        note_line._compute_is_set_desc_lines()

        self.assertTrue(note_line.is_set_desc_lines)
