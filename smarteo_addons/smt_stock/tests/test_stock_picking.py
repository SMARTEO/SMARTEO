# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestStockPickingExportAction(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        picking_type = cls.env.ref("stock.picking_type_in")
        cls.picking = cls.env["stock.picking"].create(
            {
                "picking_type_id": picking_type.id,
                "location_id": picking_type.default_location_src_id.id
                or cls.env.ref("stock.stock_location_suppliers").id,
                "location_dest_id": picking_type.default_location_dest_id.id
                or cls.env.ref("stock.stock_location_stock").id,
            }
        )

    def test_exp_button_returns_url_action_with_picking_ids(self):
        action = self.picking.exp_button()

        self.assertEqual(action["type"], "ir.actions.act_url")
        self.assertIn(str(self.picking.id), action["url"])
        self.assertTrue(action["url"].startswith("/stock_picking/export/xlsx?ids="))
