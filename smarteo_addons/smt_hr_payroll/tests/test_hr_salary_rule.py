from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestHrSalaryRuleComputeBaseNombre(TransactionCase):
    """_compute_base()/_compute_nombre() call
    safe_eval(code, localdict, mode="exec", nocopy=True), but this Odoo
    version's safe_eval() no longer accepts a `nocopy` keyword at all
    (see odoo/tools/safe_eval.py). Every call with a non-empty
    salary_rule_base/salary_rule_nombre currently raises a UserError
    wrapping that TypeError, regardless of whether the configured Python
    snippet is itself valid. These tests document that current, broken
    behavior; only the "not configured" short-circuit (which returns before
    calling safe_eval) still works as intended.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.struct = cls.env.ref("hr_payroll.structure_002")
        cls.category = cls.env.ref("hr_payroll.BASIC")
        cls.rule = cls.env["hr.salary.rule"].create(
            {
                "name": "Custom Report Rule",
                "code": "CUSTOMREPORT",
                "struct_id": cls.struct.id,
                "category_id": cls.category.id,
                "salary_rule_base": "result = 100.0 + 50.0",
                "salary_rule_nombre": "result = 3.0 * 2",
            }
        )

    def test_compute_base_currently_raises_due_to_safe_eval_signature(self):
        with self.assertRaises(UserError):
            self.rule._compute_base({})

    def test_compute_nombre_currently_raises_due_to_safe_eval_signature(self):
        with self.assertRaises(UserError):
            self.rule._compute_nombre({})

    def test_compute_base_returns_zero_when_not_configured(self):
        self.rule.salary_rule_base = False

        self.assertEqual(self.rule._compute_base({}), 0.0)

    def test_compute_nombre_returns_zero_when_not_configured(self):
        self.rule.salary_rule_nombre = False

        self.assertEqual(self.rule._compute_nombre({}), 0.0)
