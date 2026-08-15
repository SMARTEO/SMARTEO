# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestProductValue(TransactionCase):

    def test_categ_id_and_default_code_follow_product(self):
        category = self.env['product.category'].create({'name': 'Valuation Category'})
        product = self.env['product.product'].create({
            'name': 'Valued Item',
            'type': 'consu',
            'is_storable': True,
            'categ_id': category.id,
            'default_code': 'REF-001',
        })

        product_value = self.env['product.value'].create({
            'product_id': product.id,
            'company_id': self.env.company.id,
            'value': 42.0,
        })

        self.assertEqual(product_value.categ_id, category)
        self.assertEqual(product_value.default_code, 'REF-001')

    def test_categ_id_updates_when_product_category_changes(self):
        category_a = self.env['product.category'].create({'name': 'Category A'})
        category_b = self.env['product.category'].create({'name': 'Category B'})
        product = self.env['product.product'].create({
            'name': 'Movable Category Item',
            'type': 'consu',
            'is_storable': True,
            'categ_id': category_a.id,
        })
        product_value = self.env['product.value'].create({
            'product_id': product.id,
            'company_id': self.env.company.id,
            'value': 10.0,
        })
        self.assertEqual(product_value.categ_id, category_a)

        product.categ_id = category_b.id

        self.assertEqual(product_value.categ_id, category_b)
