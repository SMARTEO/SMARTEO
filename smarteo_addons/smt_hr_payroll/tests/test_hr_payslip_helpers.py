from datetime import date

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayslipPureHelpers(TransactionCase):
    """These helpers only use their arguments, so they can be called on an
    empty hr.payslip recordset without creating any record."""

    def test_get_seniority_contract_years_and_months(self):
        result = self.env["hr.payslip"].get_seniority_contract(date(2020, 3, 1), date(2026, 8, 1))

        self.assertEqual(result, "6 year(s) and 5 month(s)")

    def test_get_seniority_contract_months_only(self):
        result = self.env["hr.payslip"].get_seniority_contract(date(2026, 5, 1), date(2026, 8, 1))

        self.assertEqual(result, "3 month(s)")

    def test_get_seniority_contract_empty_start_date(self):
        result = self.env["hr.payslip"].get_seniority_contract(False, date(2026, 8, 1))

        self.assertEqual(result, "")

    def test_get_age_computed_from_year_difference(self):
        result = self.env["hr.payslip"].get_age(date(1990, 6, 15), date(2026, 8, 1))

        self.assertEqual(result, 36)

    def test_get_age_returns_zero_without_birth_date(self):
        result = self.env["hr.payslip"].get_age(False, date(2026, 8, 1))

        self.assertEqual(result, 0)

    def test_get_spent_monthly_hours_converts_weekly_to_monthly(self):
        result = self.env["hr.payslip"].get_spent_monthly_hours(40)

        self.assertAlmostEqual(result, 173.33, places=2)

    def test_get_spent_monthly_hours_returns_zero_when_falsy(self):
        result = self.env["hr.payslip"].get_spent_monthly_hours(0)

        self.assertEqual(result, 0)
