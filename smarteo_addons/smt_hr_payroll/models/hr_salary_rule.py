from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class HrSalaryRule(models.Model):
    _inherit = "hr.salary.rule"
    _description = "Salary Rule"

    salary_rule_nombre = fields.Text(
        string="Nombre", help="Value for 'nombre' in the payslip report"
    )
    salary_rule_base = fields.Text(string="Base", help="Value for 'base' in the payslip report")
    is_total = fields.Boolean(string="Total", help="Marks a rule as a totals line in the report")
    currency_salary_rule_nombre = fields.Char(
        string="Currency (Nombre)",
        default=lambda self: self.env.company.currency_id.symbol,
    )
    currency_salary_rule_base = fields.Char(
        string="Currency (Base)",
        default=lambda self: self.env.company.currency_id.symbol,
    )

    def _compute_base(self, localdict):
        self.ensure_one()
        if not self.salary_rule_base:
            return 0.0
        try:
            safe_eval(self.salary_rule_base, localdict, mode="exec", nocopy=True)
            return float(localdict["result"])
        except Exception as e:
            raise UserError(
                self.env._(
                    "Wrong Python code for base rule %(name)s (%(code)s).\nError: %(error)s",
                    name=self.name,
                    code=self.code,
                    error=e,
                )
            ) from e

    def _compute_nombre(self, localdict):
        self.ensure_one()
        if not self.salary_rule_nombre:
            return 0.0
        try:
            safe_eval(self.salary_rule_nombre, localdict, mode="exec", nocopy=True)
            return float(localdict["result"])
        except Exception as e:
            raise UserError(
                self.env._(
                    "Wrong Python code for nombre rule %(name)s (%(code)s).\nError: %(error)s",
                    name=self.name,
                    code=self.code,
                    error=e,
                )
            ) from e
