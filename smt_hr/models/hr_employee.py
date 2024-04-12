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

    cnaps = fields.Char()
    ostie = fields.Char()
    matricule = fields.Char()
    classification_id = fields.Many2one('hr.classification')
    children_ids = fields.One2many('hr.child', 'employe_id', string="Enfants à charge", store=1)

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"

    cnaps = fields.Char()
    ostie = fields.Char()
    matricule = fields.Char()

class HrEmployeeClassification(models.Model):
    _name = 'hr.classification'

    name = fields.Char()