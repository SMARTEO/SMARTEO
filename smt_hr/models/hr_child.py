from odoo import fields, models, api, _
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class HrChildren(models.Model):
    _name = 'hr.child'
    _description = 'Description'
    employe_id = fields.Many2one('hr.employee')
    name = fields.Char(string="Nom")
    child_age = fields.Integer(string="Age", compute='_compute_age', store=True)
    birthday = fields.Date('Date de naissance')
    state = fields.Selection([('dependent', 'à charge'),
                              ('not_dependent', 'Pas à charge')
                              ])

    @api.depends('birthday')
    def _compute_age(self):
        for chield in self:
            if chield.birthday:
                chield.write({'child_age': relativedelta(date.today(), chield.birthday).years})
                if chield.child_age > 21:
                    chield.state = 'not_dependent'
                else:
                    chield.state = 'dependent'
            else:
                chield.child_age = 0

