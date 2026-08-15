from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAccountPaymentTerm(TransactionCase):
    def test_default_description_and_payment_method_round_trip(self):
        term = self.env["account.payment.term"].create(
            {
                "name": "Test Term",
                "default_description": True,
                "payment_method": "check",
            }
        )

        self.assertTrue(term.default_description)
        self.assertEqual(term.payment_method, "check")

    def test_payment_method_defaults_to_false(self):
        term = self.env["account.payment.term"].create({"name": "Untouched Term"})

        self.assertFalse(term.payment_method)
