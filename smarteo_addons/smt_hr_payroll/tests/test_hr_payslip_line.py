# -*- coding: utf-8 -*-
from datetime import date

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayslipLine(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.struct = cls.env.ref("hr_payroll.structure_002")
        cls.category = cls.env.ref("hr_payroll.BASIC")
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Line Test Employee",
                "wage": 1000,
            }
        )
        cls.rule = cls.env["hr.salary.rule"].create(
            {
                "name": "Line Test Rule",
                "code": "LINETEST",
                "struct_id": cls.struct.id,
                "category_id": cls.category.id,
            }
        )
        # gain_on_current_month must be falsy at creation time, and
        # previous_paid_leave_balance must be given explicitly: see the
        # dedicated regression tests in test_hr_payslip.py for why (both
        # otherwise hit pre-existing bugs unrelated to what's tested here).
        cls.payslip = cls.env["hr.payslip"].create(
            {
                "name": "Line Test Payslip",
                "employee_id": cls.employee.id,
                "date_from": date(2026, 1, 1),
                "date_to": date(2026, 1, 31),
                "struct_id": cls.struct.id,
                "gain_on_current_month": False,
                "previous_paid_leave_balance": 0,
            }
        )

    def test_nombre_and_base_default_to_zero(self):
        line = self.env["hr.payslip.line"].create(
            {
                "name": "Line Test Rule",
                "slip_id": self.payslip.id,
                "salary_rule_id": self.rule.id,
                "version_id": self.payslip.version_id.id,
                "employee_id": self.employee.id,
            }
        )

        self.assertEqual(line.nombre, 0)
        self.assertEqual(line.base, 0)

    def test_nombre_and_base_round_trip(self):
        line = self.env["hr.payslip.line"].create(
            {
                "name": "Line Test Rule",
                "slip_id": self.payslip.id,
                "salary_rule_id": self.rule.id,
                "version_id": self.payslip.version_id.id,
                "employee_id": self.employee.id,
                "nombre": 21.0,
                "base": 1500.0,
            }
        )

        self.assertEqual(line.nombre, 21.0)
        self.assertEqual(line.base, 1500.0)

    def test_category_code_follows_salary_rule_category(self):
        line = self.env["hr.payslip.line"].create(
            {
                "name": "Line Test Rule",
                "slip_id": self.payslip.id,
                "salary_rule_id": self.rule.id,
                "version_id": self.payslip.version_id.id,
                "employee_id": self.employee.id,
            }
        )

        self.assertEqual(line.category_code, self.category.code)
