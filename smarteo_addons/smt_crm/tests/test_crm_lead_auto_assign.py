from odoo.tests.common import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestCrmLeadAutoAssign(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.salesperson = new_test_user(cls.env, login="salesperson_for_customer")
        cls.commande_team = cls.env["crm.team"].create(
            {"name": "Service Commercial", "alias_name": "commande"}
        )
        cls.other_team = cls.env["crm.team"].create(
            {"name": "Website", "alias_name": "website_leads"}
        )

    def _create_lead(self, team, email_from, partner=None):
        # Mirrors mail.thread.message_new(), which creates userless leads by
        # forcing default_user_id=False instead of the acting (gateway) user.
        return (
            self.env["crm.lead"]
            .with_context(default_user_id=False)
            .create(
                {
                    "name": "Incoming request",
                    "type": "lead",
                    "team_id": team.id,
                    "email_from": email_from,
                    "partner_id": partner.id if partner else False,
                }
            )
        )

    def test_assigned_to_matching_company_salesperson(self):
        company = self.env["res.partner"].create(
            {
                "name": "Acme Corp",
                "is_company": True,
                "email": "contact@acme.example",
                "user_id": self.salesperson.id,
            }
        )
        lead = self._create_lead(self.commande_team, "contact@acme.example")

        lead._assign_userless_lead_in_team("test")

        self.assertEqual(lead.user_id, self.salesperson)
        self.assertEqual(lead.partner_id, company)

    def test_assigned_to_matching_individual_salesperson(self):
        individual = self.env["res.partner"].create(
            {
                "name": "Jean Dupont",
                "email": "jean.dupont@example.com",
                "user_id": self.salesperson.id,
            }
        )
        lead = self._create_lead(self.commande_team, "jean.dupont@example.com")

        lead._assign_userless_lead_in_team("test")

        self.assertEqual(lead.user_id, self.salesperson)
        self.assertEqual(lead.partner_id, individual)

    def test_individual_without_own_salesperson_inherits_company_one(self):
        company = self.env["res.partner"].create(
            {
                "name": "Acme Corp",
                "is_company": True,
                "user_id": self.salesperson.id,
            }
        )
        contact = self.env["res.partner"].create(
            {
                "name": "Jean Dupont",
                "email": "jean.dupont@acme.example",
                "parent_id": company.id,
            }
        )
        self.assertEqual(contact.user_id, self.salesperson)  # parent fallback (res.partner core)
        lead = self._create_lead(self.commande_team, "jean.dupont@acme.example")

        lead._assign_userless_lead_in_team("test")

        self.assertEqual(lead.user_id, self.salesperson)

    def test_new_client_stays_unassigned(self):
        lead = self._create_lead(self.commande_team, "unknown@example.com")

        lead._assign_userless_lead_in_team("test")

        self.assertFalse(lead.user_id)

    def test_matched_partner_without_salesperson_stays_unassigned(self):
        self.env["res.partner"].create(
            {"name": "Acme Corp", "is_company": True, "email": "contact@acme.example"}
        )
        lead = self._create_lead(self.commande_team, "contact@acme.example")

        lead._assign_userless_lead_in_team("test")

        self.assertFalse(lead.user_id)

    def test_team_id_unchanged_when_salesperson_is_not_a_team_member(self):
        # crm.lead.team_id is computed from user_id (see crm._compute_team_id) and
        # would otherwise drift to the salesperson's own default team.
        self.assertNotIn(self.salesperson, self.commande_team.member_ids)
        self.env["res.partner"].create(
            {
                "name": "Acme Corp",
                "is_company": True,
                "email": "contact@acme.example",
                "user_id": self.salesperson.id,
            }
        )
        lead = self._create_lead(self.commande_team, "contact@acme.example")

        lead._assign_userless_lead_in_team("test")

        self.assertEqual(lead.team_id, self.commande_team)
        self.assertEqual(lead.user_id, self.salesperson)

    def test_other_team_leads_keep_stock_team_leader_fallback(self):
        self.other_team.user_id = self.salesperson
        lead = self._create_lead(self.other_team, "unknown@example.com")

        lead._assign_userless_lead_in_team("test")

        self.assertEqual(lead.user_id, self.salesperson)
