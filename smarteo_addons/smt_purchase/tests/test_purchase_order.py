# -*- coding: utf-8 -*-
from datetime import datetime

from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestPurchaseOrderCombinedDate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vendor = cls.env['res.partner'].create({'name': 'Test Vendor'})

    def test_combined_date_empty_when_no_date_order(self):
        order = self.env['purchase.order'].create({'partner_id': self.vendor.id})
        order.date_order = False

        order._compute_combined_date()

        self.assertEqual(order.dateorder_dateapprove, "")

    def test_combined_date_uses_date_order_when_not_approved(self):
        order = self.env['purchase.order'].create({'partner_id': self.vendor.id})
        order.date_order = datetime(2026, 3, 15, 10, 0, 0)

        order._compute_combined_date()

        self.assertEqual(order.dateorder_dateapprove, '15-03-2026')

    def test_combined_date_prefers_date_approve_when_set(self):
        order = self.env['purchase.order'].create({'partner_id': self.vendor.id})
        order.date_order = datetime(2026, 3, 15, 10, 0, 0)
        order.date_approve = datetime(2026, 3, 20, 8, 30, 0)

        order._compute_combined_date()

        self.assertEqual(order.dateorder_dateapprove, '20-03-2026')
