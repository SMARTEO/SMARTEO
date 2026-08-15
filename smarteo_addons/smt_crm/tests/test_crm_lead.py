from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCrmLeadMoveToLost(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["crm.stage"].search([("is_lost", "=", True)]).write({"is_lost": False})
        cls.open_stage = cls.env["crm.stage"].create({"name": "Open"})

    def test_raises_when_no_lost_stage_configured(self):
        with self.assertRaises(ValidationError):
            self.env["crm.lead"]._move_opportunities_to_lost_stage()

    def test_moves_inactive_zero_probability_leads_to_lost_stage(self):
        lost_stage = self.env["crm.stage"].create({"name": "Lost", "is_lost": True})
        lead = self.env["crm.lead"].create(
            {
                "name": "Dead opportunity",
                "type": "opportunity",
                "stage_id": self.open_stage.id,
                "probability": 0,
                "active": False,
            }
        )

        self.env["crm.lead"]._move_opportunities_to_lost_stage()

        self.assertEqual(lead.stage_id, lost_stage)

    def test_leaves_active_leads_untouched(self):
        self.env["crm.stage"].create({"name": "Lost", "is_lost": True})
        active_lead = self.env["crm.lead"].create(
            {
                "name": "Still alive",
                "type": "opportunity",
                "stage_id": self.open_stage.id,
                "probability": 0,
            }
        )

        self.env["crm.lead"]._move_opportunities_to_lost_stage()

        self.assertEqual(active_lead.stage_id, self.open_stage)

    def test_leaves_leads_with_nonzero_probability_untouched(self):
        self.env["crm.stage"].create({"name": "Lost", "is_lost": True})
        lead = self.env["crm.lead"].create(
            {
                "name": "Still has a chance",
                "type": "opportunity",
                "stage_id": self.open_stage.id,
                "probability": 20,
                "active": False,
            }
        )

        self.env["crm.lead"]._move_opportunities_to_lost_stage()

        self.assertEqual(lead.stage_id, self.open_stage)
