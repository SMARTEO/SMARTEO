from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestCrmStageVisibility(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stage = cls.env["crm.stage"].create({"name": "Hidden Stage"})
        cls.lead = cls.env["crm.lead"].create(
            {
                "name": "Some opportunity",
                "type": "opportunity",
                "stage_id": cls.stage.id,
            }
        )
        # "All Leads" access grants an ir.rule of [(1,'=',1)], which would
        # normally OR-override any group-scoped restriction. The visibility
        # rule must stay effective even for a user holding this group.
        cls.user = new_test_user(
            cls.env,
            login="restricted_salesperson",
            groups="sales_team.group_sale_salesman_all_leads",
        )

    def test_lead_visible_by_default(self):
        found = self.env["crm.lead"].with_user(self.user).search([("id", "=", self.lead.id)])
        self.assertEqual(found, self.lead)

    def test_lead_hidden_once_user_is_restricted_on_stage(self):
        self.stage.restricted_user_ids = [(6, 0, self.user.ids)]

        found = self.env["crm.lead"].with_user(self.user).search([("id", "=", self.lead.id)])

        self.assertFalse(found)

    def test_other_users_unaffected_by_restriction(self):
        other_user = new_test_user(
            self.env,
            login="unrestricted_salesperson",
            groups="sales_team.group_sale_salesman_all_leads",
        )
        self.stage.restricted_user_ids = [(6, 0, self.user.ids)]

        found = self.env["crm.lead"].with_user(other_user).search([("id", "=", self.lead.id)])

        self.assertEqual(found, self.lead)

    def test_lead_visible_again_once_unrestricted(self):
        self.stage.restricted_user_ids = [(6, 0, self.user.ids)]
        self.stage.restricted_user_ids = [(5, 0, 0)]

        found = self.env["crm.lead"].with_user(self.user).search([("id", "=", self.lead.id)])

        self.assertEqual(found, self.lead)

    def test_kanban_column_hidden_for_restricted_user(self):
        # Odoo's stage group_expand normally shows every stage as a column,
        # even an empty one, so hiding leads alone leaves a visible empty column.
        self.stage.restricted_user_ids = [(6, 0, self.user.ids)]

        columns = (
            self.env["crm.lead"]
            .with_user(self.user)
            ._read_group_stage_ids(self.env["crm.stage"], [])
        )

        self.assertNotIn(self.stage, columns)

    def test_kanban_column_visible_for_unrestricted_user(self):
        other_user = new_test_user(
            self.env,
            login="unrestricted_salesperson_kanban",
            groups="sales_team.group_sale_salesman_all_leads",
        )
        self.stage.restricted_user_ids = [(6, 0, self.user.ids)]

        columns = (
            self.env["crm.lead"]
            .with_user(other_user)
            ._read_group_stage_ids(self.env["crm.stage"], [])
        )

        self.assertIn(self.stage, columns)
