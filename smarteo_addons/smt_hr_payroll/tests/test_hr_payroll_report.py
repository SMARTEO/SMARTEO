# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayrollReport(TransactionCase):
    def test_report_view_is_queryable(self):
        # hr.payroll.report is a SQL view (_auto=False); this mainly checks
        # that init() built valid SQL and the model can be searched/read
        # without a database error, even with no payslips in 'done'/'paid'
        # state yet.
        report_lines = self.env["hr.payroll.report"].search([])

        self.assertEqual(list(report_lines), [])
