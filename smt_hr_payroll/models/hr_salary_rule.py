# -*- coding:utf-8 -*-


from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class HrSalaryRule(models.Model):
    _inherit = "hr.salary.rule"

    salary_rule_nombre = fields.Text(
        string="Nombre", help="La valeur de nombre dans la structure de base"
    )
    salary_rule_base = fields.Text(
        string="Base", help="La valeur de base dans la structure de base"
    )

    is_total = fields.Boolean(string="Total", help="Pour faciliter le format du report")


    currency_name = fields.Char(compute='_get_currency_name')

    def _get_currency_name(self):
        self.ensure_one()
        self.currency_name = self.env.company.currency_id.symbol

    def write(self, vals):
        res = super().write(vals)
        return res

    def _compute_base(self, localdict):
        self.ensure_one()
        if self.salary_rule_base:
            try:
                safe_eval(
                    self.salary_rule_base or 0.0,
                    localdict,
                    mode="exec",
                    nocopy=True,
                    )
                return float(localdict["result"])
            except Exception as e:
                raise UserError(
                    _("Wrong python code defined for base rule %s (%s).\nError: %s")
                    % (self.name, self.code, e)
                )

    def _compute_nombre(self, localdict):
        self.ensure_one()
        if self.salary_rule_nombre:
            try:
                safe_eval(
                    self.salary_rule_nombre or 0.0,
                    localdict,
                    mode="exec",
                    nocopy=True,
                    )
                return float(localdict["result"])
            except Exception as e:
                raise UserError(
                    _("Wrong python code defined for nombre rule %s (%s).\nError: %s")
                    % (self.name, self.code, e)
                )
