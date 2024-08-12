# -*- coding:utf-8 -*-

from odoo import fields, models


class HrPayslipInput(models.Model):
    _inherit = 'hr.payslip.input'

    code = fields.Char(related='input_type_id.code', required=True, help="The code that can be used in the salary rules",store=True)
