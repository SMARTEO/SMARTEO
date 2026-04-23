# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class HrPayslipInputTypeInherit(models.Model):
    _inherit = "hr.payslip.input.type"
    _description = 'Payslip Input Type'

    generate = fields.Boolean(default=False, string="Generate")
