# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestCrmStage(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Any pre-existing lost stage would make these tests order-dependent.
        cls.env['crm.stage'].search([('is_lost', '=', True)]).write({'is_lost': False})

    def test_first_lost_stage_is_allowed(self):
        stage = self.env['crm.stage'].create({'name': 'Lost', 'is_lost': True})
        self.assertTrue(stage.is_lost)

    def test_second_lost_stage_raises(self):
        self.env['crm.stage'].create({'name': 'Lost', 'is_lost': True})

        with self.assertRaises(ValidationError):
            self.env['crm.stage'].create({'name': 'Also Lost', 'is_lost': True})

    def test_marking_existing_stage_as_lost_raises_when_one_exists(self):
        self.env['crm.stage'].create({'name': 'Lost', 'is_lost': True})
        other_stage = self.env['crm.stage'].create({'name': 'In Progress'})

        with self.assertRaises(ValidationError):
            other_stage.is_lost = True

    def test_multiple_non_lost_stages_are_allowed(self):
        self.env['crm.stage'].create({'name': 'Stage A'})
        self.env['crm.stage'].create({'name': 'Stage B'})
        # No exception expected.
