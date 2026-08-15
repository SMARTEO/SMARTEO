from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class HrChild(models.Model):
    _name = "hr.child"
    _description = "Employee Dependant Child"

    employe_id = fields.Many2one("hr.employee", string="Employee")
    employe_public_id = fields.Many2one("hr.employee.public", string="Employee (Public)")
    name = fields.Char(string="Name")
    birthday = fields.Date(string="Date of Birth")
    child_age = fields.Integer(string="Age", compute="_compute_age", store=True)
    state = fields.Selection(
        [
            ("dependent", "Dependant"),
            ("not_dependent", "Not Dependant"),
        ],
        string="Status",
    )

    @api.depends("birthday")
    def _compute_age(self):
        today = date.today()
        for child in self:
            if child.birthday:
                child.child_age = relativedelta(today, child.birthday).years
                child.state = "not_dependent" if child.child_age > 21 else "dependent"
            else:
                child.child_age = 0
