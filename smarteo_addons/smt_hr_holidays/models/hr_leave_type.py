from odoo import fields, models


class HolidaysType(models.Model):
    _inherit = "hr.leave.type"
    _description = "Time Off Type"

    is_of_the_paid_leave_type = fields.Boolean()
