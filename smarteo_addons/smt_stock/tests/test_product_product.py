# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductProductValues(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.location = cls.env.ref("stock.stock_location_stock")
        cls.product = cls.env["product.product"].create(
            {
                "name": "Valued Product",
                "type": "consu",
                "is_storable": True,
                "standard_price": 25.0,
            }
        )

    def test_values_is_zero_without_stock(self):
        self.product._compute_values()

        self.assertEqual(self.product.values, 0.0)

    def test_values_matches_quantity_times_standard_price(self):
        self.env["stock.quant"]._update_available_quantity(self.product, self.location, 10.0)

        self.product._compute_values()

        self.assertEqual(self.product.qty_available, 10.0)
        self.assertEqual(self.product.values, 250.0)
