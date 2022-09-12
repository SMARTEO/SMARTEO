# -*- coding: utf-8 -*-

from ast import Store
from odoo import models, fields, api


class HrEmployeeInherit(models.Model):
    _inherit = "hr.employee"

    phone = fields.Char(
        string="Téléphone",
        groups="hr.group_hr_user",
        store=True,
    )

    private_email = fields.Char(
        string="Courriel",
        groups="hr.group_hr_user",
        store=True,
    )
