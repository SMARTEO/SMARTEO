# -*- coding: utf-8 -*-
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = 'Employee'

    phone = fields.Char(
        string="Phone",
        groups="hr.group_hr_user",
        store=True,
    )
    private_email = fields.Char(
        string="Email",
        groups="hr.group_hr_user",
        store=True,
    )
    cnaps = fields.Char(string="CNAPS No.")
    ostie = fields.Char(string="OSTIE No.")
    matricule = fields.Char(string="Employee ID")
    classification_id = fields.Many2one('hr.classification', string="Classification")
    children_ids = fields.One2many('hr.child', 'employe_id', string="Dependant Children", store=True)


class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"
    _description = 'Employee (Public)'

    cnaps = fields.Char(string="CNAPS No.")
    ostie = fields.Char(string="OSTIE No.")
    matricule = fields.Char(string="Employee ID")
    classification_id = fields.Many2one('hr.classification', string="Classification")
    children_ids = fields.One2many('hr.child', 'employe_public_id', string="Dependant Children", store=True)


class HrClassification(models.Model):
    _name = 'hr.classification'
    _description = 'Employee Classification'

    name = fields.Char(string="Name", required=True)
