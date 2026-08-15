# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResPartnerCompete(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.competitor = cls.env["res.partner"].create(
            {
                "name": "Competitor Corp",
                "compete": False,
            }
        )
        cls.child_of_competitor = cls.env["res.partner"].create(
            {
                "name": "Competitor Corp Branch",
                "parent_id": cls.competitor.id,
                "compete": False,
            }
        )
        cls.non_competitor = cls.env["res.partner"].create(
            {
                "name": "Friendly Corp",
                "compete": False,
            }
        )
        cls.child_of_non_competitor = cls.env["res.partner"].create(
            {
                "name": "Friendly Corp Branch",
                "parent_id": cls.non_competitor.id,
                "compete": False,
            }
        )

    def test_tax_identifier_fields_round_trip(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Malagasy Company",
                "nif": "NIF-001",
                "stat": "STAT-001",
                "rcs": "RCS-001",
                "cif": "CIF-001",
                "customer": True,
                "supplier": True,
            }
        )
        self.assertEqual(partner.nif, "NIF-001")
        self.assertEqual(partner.stat, "STAT-001")
        self.assertEqual(partner.rcs, "RCS-001")
        self.assertEqual(partner.cif, "CIF-001")
        self.assertTrue(partner.customer)
        self.assertTrue(partner.supplier)

    def test_update_compete_for_child_propagates_to_children(self):
        self.competitor.compete = True

        self.competitor.update_compete_for_child()

        self.assertTrue(self.child_of_competitor.compete)

    def test_update_compete_for_child_leaves_other_children_untouched(self):
        self.competitor.compete = True

        self.competitor.update_compete_for_child()

        self.assertFalse(self.child_of_non_competitor.compete)

    def test_update_compete_for_child_noop_when_no_competitor(self):
        self.non_competitor.update_compete_for_child()

        self.assertFalse(self.child_of_non_competitor.compete)

    def test_onchange_compete_sets_children_when_flag_raised(self):
        self.competitor.compete = True

        self.competitor._onchange_compete()

        self.assertTrue(self.child_of_competitor.compete)

    def test_onchange_compete_does_nothing_when_flag_not_set(self):
        self.competitor._onchange_compete()

        self.assertFalse(self.child_of_competitor.compete)
