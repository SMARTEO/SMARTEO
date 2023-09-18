# -*- coding: utf-8 -*-


from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.osv import expression

class Contract(models.Model):
    _inherit = "hr.contract"

    classification_id = fields.Many2one(related='employee_id.classification_id', readonly=True, store=True)

    hour_per_week = fields.Float(
        string="Nombre d'heures travaillé par semaine", related="resource_calendar_id.full_time_required_hours",
        required=True)
    base_salary = fields.Monetary('Salaire de base')
    hourly_salary = fields.Monetary('Salaire horaire ', compute='_get_hourly_salary')
    month_12_last_salary = fields.Monetary('Salaire moyen des 12 derniers mois')
    allow_transport = fields.Monetary('Indemnité de transport')
    allow_family = fields.Monetary('Allocations familiales')
    allow_logement = fields.Monetary('Indemnité de logement')
    other_allow = fields.Monetary('Autres ndemnités')
    wage = fields.Monetary('Wage', required=True, tracking=True, help="Employee's monthly gross wage.",
                           compute='_compute_base_salary')

    def _compute_base_salary(self):
        for record in self:
            record.wage = record.base_salary

    @api.depends('hour_per_week')
    def _get_hourly_salary(self):
        for rec in self:
            if rec.hour_per_week:
                rec.hourly_salary = rec.base_salary / ((rec.hour_per_week * 52) / 12)
            else:
                rec.hourly_salary = 0