from odoo import fields, models


class HrPayslipLine(models.Model):
    _inherit = "hr.payslip.line"
    _description = "Payslip Line"

    nombre = fields.Float(string="Nombre", default=0)
    base = fields.Float(string="Base", default=0)
    category_code = fields.Char(related="category_id.code", string="Category Code")
