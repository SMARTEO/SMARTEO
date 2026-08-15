# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Contract(models.Model):
    _inherit = "hr.version"
    _description = "Employee Contract Version"

    classification_id = fields.Many2one(
        related="employee_id.classification_id",
        string="Classification",
        readonly=True,
        store=True,
    )
    hour_per_week = fields.Float(
        string="Weekly Hours",
        related="resource_calendar_id.full_time_required_hours",
        required=True,
    )
    base_salary = fields.Monetary(string="Base Salary")
    hourly_salary = fields.Monetary(string="Hourly Salary", compute="_compute_hourly_salary")
    month_12_last_salary = fields.Monetary(string="Average Salary (Last 12 Months)")
    allow_transport = fields.Monetary(string="Transport Allowance")
    allow_family = fields.Monetary(string="Family Allowance")
    allow_logement = fields.Monetary(string="Meal Allowance")
    other_allow = fields.Monetary(string="Other Allowances")
    wage = fields.Monetary(
        string="Wage",
        required=True,
        tracking=True,
        help="Employee's monthly gross wage.",
        compute="_compute_wage",
        store=True,
    )

    @api.depends("base_salary")
    def _compute_wage(self):
        for record in self:
            record.wage = record.base_salary

    @api.depends("base_salary", "hour_per_week")
    def _compute_hourly_salary(self):
        for rec in self:
            if rec.hour_per_week:
                rec.hourly_salary = rec.base_salary / ((rec.hour_per_week * 52) / 12)
            else:
                rec.hourly_salary = 0
