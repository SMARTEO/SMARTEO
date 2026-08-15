# -*- coding: utf-8 -*-
from datetime import date

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrPayslipInput(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.struct = cls.env.ref("hr_payroll.structure_002")
        cls.input_type = cls.env.ref("hr_payroll.input_reimbursement")
        cls.employee = cls.env["hr.employee"].create(
            {
                "name": "Input Test Employee",
                "wage": 1000,
            }
        )
        cls.payslip = cls.env["hr.payslip"].create(
            {
                "name": "Input Test Payslip",
                "employee_id": cls.employee.id,
                "date_from": date(2026, 1, 1),
                "date_to": date(2026, 1, 31),
                "struct_id": cls.struct.id,
                "gain_on_current_month": False,
                "previous_paid_leave_balance": 0,
            }
        )

    def test_code_mirrors_input_type_code(self):
        payslip_input = self.env["hr.payslip.input"].create(
            {
                "payslip_id": self.payslip.id,
                "input_type_id": self.input_type.id,
                "amount": 50.0,
            }
        )

        self.assertEqual(payslip_input.code, self.input_type.code)

    def test_code_updates_when_input_type_changes(self):
        other_type = self.env.ref("hr_payroll.input_deduction")
        payslip_input = self.env["hr.payslip.input"].create(
            {
                "payslip_id": self.payslip.id,
                "input_type_id": self.input_type.id,
                "amount": 50.0,
            }
        )

        payslip_input.input_type_id = other_type.id

        self.assertEqual(payslip_input.code, other_type.code)
