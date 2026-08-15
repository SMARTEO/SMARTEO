from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestStockQuantValues(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.location = cls.env.ref("stock.stock_location_stock")
        cls.category = cls.env["product.category"].create({"name": "Test Category"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Quant Product",
                "type": "consu",
                "is_storable": True,
                "standard_price": 12.5,
                "categ_id": cls.category.id,
            }
        )
        cls.env["stock.quant"]._update_available_quantity(cls.product, cls.location, 8.0)
        cls.quant = cls.env["stock.quant"].search(
            [
                ("product_id", "=", cls.product.id),
                ("location_id", "=", cls.location.id),
            ],
            limit=1,
        )

    def test_related_standard_price_and_category(self):
        self.assertEqual(self.quant.standard_price, 12.5)
        self.assertEqual(self.quant.category_id, self.category)

    def test_values_matches_auto_apply_quantity_times_standard_price(self):
        self.quant._compute_values()

        self.assertEqual(self.quant.inventory_quantity_auto_apply, 8.0)
        self.assertEqual(self.quant.values, 100.0)

    def test_values_follows_standard_price_change(self):
        self.product.standard_price = 20.0

        self.quant._compute_values()

        self.assertEqual(self.quant.values, 160.0)
