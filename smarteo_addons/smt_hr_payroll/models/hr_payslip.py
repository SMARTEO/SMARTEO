# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from odoo.tools.date_utils import get_timedelta

from odoo import api, fields, models, _
from odoo.tools import html2plaintext

# HOURS_PER_DAY moved between Odoo versions; fall back to 8.0 if import fails.
try:
    from odoo.addons.resource.models.resource import HOURS_PER_DAY
except ImportError:
    try:
        from odoo.addons.resource.models.utils import HOURS_PER_DAY
    except ImportError:
        HOURS_PER_DAY = 8.0


class HrPayslip(models.Model):
    _inherit = "hr.payslip"
    _description = 'Payslip'

    commentaire = fields.Text(string="Comment")
    paid_date = fields.Date(string="Payment Date", readonly=True)
    is_balance_all_account = fields.Boolean(string="Full Account Balance")
    balance_to_date = fields.Float(string="Balance to Date")
    gain_on_current_month = fields.Selection(
        [('0', '0'), ('2.5', '2.5')],
        string="Monthly Accrual",
        default='2.5',
    )
    balance_on_pay_slip = fields.Float(string="Balance on Payslip")
    payment_method_in_pdf = fields.Char(string="Payment Method (PDF)")
    is_can_modif_all_balance = fields.Boolean(compute='_compute_is_can_modif_all_balance')
    previous_paid_leave_balance = fields.Float(
        compute="compute_previous_paid_leave_balance",
        store=True,
        readonly=False,
        string="Previous Paid Leave Balance",
    )
    days_taken_in_the_month = fields.Float(
        compute='_compute_days_taken_in_the_month',
        string="Days Taken This Month",
    )
    new_balance_in_the_month = fields.Float(
        compute='_compute_new_balance_in_the_month',
        string="New Balance This Month",
    )

    def _compute_is_can_modif_all_balance(self):
        can = self.env.user.has_group('smt_hr_payroll.group_can_modif_balance_payroll')
        for slip in self:
            slip.is_can_modif_all_balance = can

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for payslip in res:
            if payslip.employee_id and payslip.gain_on_current_month:
                payslip.balance_to_date = payslip.employee_id.leaves_count
                if payslip.gain_on_current_month == '2.5':
                    payslip.balance_on_pay_slip = payslip.employee_id.leaves_count + 2.5
                else:
                    payslip.balance_on_pay_slip = payslip.employee_id.leaves_count
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'gain_on_current_month' in vals and vals['gain_on_current_month']:
            for slip in self:
                if vals['gain_on_current_month'] == '2.5':
                    slip.balance_on_pay_slip = slip.balance_to_date + 2.5
                else:
                    slip.balance_on_pay_slip = slip.balance_to_date
        return res

    @api.depends('worked_days_line_ids', 'worked_days_line_ids.work_entry_type_id',
                 'worked_days_line_ids.number_of_days')
    def _compute_days_taken_in_the_month(self):
        for paye in self:
            paye.days_taken_in_the_month = sum(
                paye.worked_days_line_ids.filtered(
                    lambda w: w.work_entry_type_id.code == 'LEAVE100'
                ).mapped('number_of_days')
            )

    @api.onchange('previous_paid_leave_balance')
    def _onchange_previous_paid_leave_balance(self):
        for paye in self:
            paye.new_balance_in_the_month = (
                paye.previous_paid_leave_balance + float(paye.gain_on_current_month)
            ) - paye.days_taken_in_the_month

    @api.depends('previous_paid_leave_balance', 'gain_on_current_month', 'days_taken_in_the_month')
    def _compute_new_balance_in_the_month(self):
        for paye in self:
            paye.new_balance_in_the_month = (
                paye.previous_paid_leave_balance + float(paye.gain_on_current_month)
            ) - paye.days_taken_in_the_month

    def calculate_cumul_leaves(self, date_ref):
        holiday_status_id = self.env.ref('hr_holidays.holiday_status_cl')
        leaves = self.env['hr.leave'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', '=', 'validate'),
            ('holiday_status_id', '=', holiday_status_id.id),
            ('request_date_from', '<', date_ref),
            ('request_date_to', '<=', date_ref),
        ])
        return sum(leaves.mapped('number_of_days'))

    def calculate_cumul_allocation(self, date_ref):
        # FIXME: The internal accrual plan API (hr.leave.accrual.level._get_next_date,
        # _get_previous_date, hr.leave.allocation._get_current_accrual_plan_level_id,
        # _process_accrual_plan_level) changed significantly in Odoo 17+.
        # This method needs to be reviewed and updated for v19 compatibility.
        holiday_status_id = self.env.ref('hr_holidays.holiday_status_cl')
        allocation_regulars = self.env['hr.leave.allocation'].search([
            ('state', '=', 'validate'),
            ('allocation_type', '=', 'regular'),
            ('holiday_status_id', '=', holiday_status_id.id),
            ('employee_id', '=', self.employee_id.id),
            ('date_from', '<=', date_ref),
            '|', ('date_to', '>=', date_ref), ('date_to', '=', False),
        ])
        allocation_accruals = self.env['hr.leave.allocation'].search([
            ('state', '=', 'validate'),
            ('allocation_type', '=', 'accrual'),
            ('holiday_status_id', '=', holiday_status_id.id),
            ('employee_id', '=', self.employee_id.id),
            ('date_from', '<=', date_ref),
            '|', ('date_to', '>=', date_ref), ('date_to', '=', False),
        ])
        level_value = 0.0
        today = fields.Date.today()
        for allocation_accrual in allocation_accruals:
            date_from = self.date_from - timedelta(days=1)
            level_ids = allocation_accrual.accrual_plan_id.level_ids.sorted('sequence')
            if not level_ids:
                continue
            first_level = level_ids[0]
            first_level_start_date = allocation_accrual.date_from + get_timedelta(
                first_level.start_count, first_level.start_type
            )
            if today < first_level_start_date:
                continue
            lastcall = first_level_start_date
            nextcall = first_level._get_next_date(lastcall)
            if len(level_ids) > 1:
                second_level_start_date = allocation_accrual.date_from + get_timedelta(
                    level_ids[1].start_count, level_ids[1].start_type
                )
                nextcall = min(second_level_start_date, nextcall)
            days_added_per_level = defaultdict(lambda: 0)
            while nextcall <= date_from:
                (current_level, current_level_idx) = allocation_accrual._get_current_accrual_plan_level_id(nextcall)
                hours_per_day = (
                    allocation_accrual.employee_id.sudo().resource_id.calendar_id.hours_per_day
                    or HOURS_PER_DAY
                )
                current_level_maximum_leave = (
                    current_level.maximum_leave
                    if current_level.added_value_type == "days"
                    else current_level.maximum_leave / hours_per_day
                )
                new_nextcall = current_level._get_next_date(nextcall)
                period_start = current_level._get_previous_date(lastcall)
                period_end = current_level._get_next_date(lastcall)
                if (
                    current_level_idx < (len(level_ids) - 1)
                    and allocation_accrual.accrual_plan_id.transition_mode == 'immediately'
                ):
                    next_level = level_ids[current_level_idx + 1]
                    current_level_last_date = allocation_accrual.date_from + get_timedelta(
                        next_level.start_count, next_level.start_type
                    )
                    if nextcall != current_level_last_date:
                        new_nextcall = min(new_nextcall, current_level_last_date)
                days_added_per_level[current_level] += allocation_accrual._process_accrual_plan_level(
                    current_level, period_start, lastcall, period_end, nextcall
                )
                if current_level_maximum_leave > 0 and sum(days_added_per_level.values()) > current_level_maximum_leave:
                    days_added_per_level[current_level] -= (
                        sum(days_added_per_level.values()) - current_level_maximum_leave
                    )
                lastcall = nextcall
                nextcall = new_nextcall
            if days_added_per_level:
                number_of_days_to_add = sum(days_added_per_level.values())
                hours_per_day = (
                    allocation_accrual.employee_id.sudo().resource_id.calendar_id.hours_per_day
                    or HOURS_PER_DAY
                )
                max_allocation_days = current_level_maximum_leave + (
                    allocation_accrual.leaves_taken
                    if allocation_accrual.type_request_unit != "hour"
                    else allocation_accrual.leaves_taken / hours_per_day
                )
                level_value += (
                    min(number_of_days_to_add, max_allocation_days)
                    if current_level_maximum_leave > 0
                    else number_of_days_to_add
                )
        return level_value + sum(allocation_regulars.mapped('number_of_days'))

    @api.depends('employee_id', 'date_from')
    def compute_previous_paid_leave_balance(self):
        for payslip in self:
            payslip.previous_paid_leave_balance = 0.0
            if payslip.employee_id:
                payslip.previous_paid_leave_balance = (
                    payslip.calculate_cumul_allocation(payslip.date_from)
                    - payslip.calculate_cumul_leaves(payslip.date_from)
                )

    def refresh_payslip_leave_situation(self):
        self._compute_days_taken_in_the_month()
        self._compute_new_balance_in_the_month()
        self.compute_previous_paid_leave_balance()

    @api.onchange('employee_id')
    def _onchange_employee_id_balance(self):
        for paye in self:
            paye.balance_to_date = paye.employee_id.leaves_count
            if paye.gain_on_current_month == '2.5':
                paye.balance_on_pay_slip = paye.balance_to_date + 2.5
            else:
                paye.balance_on_pay_slip = paye.balance_to_date

    @api.onchange('gain_on_current_month', 'employee_id')
    def _onchange_gain_on_current_month(self):
        for paye in self:
            if paye.gain_on_current_month == '2.5':
                paye.balance_on_pay_slip = paye.balance_to_date + 2.5
            else:
                paye.balance_on_pay_slip = paye.balance_to_date

    def compute_sheet(self):
        res = super().compute_sheet()
        self.write({'paid_date': fields.Date.today()})
        return res

    def get_seniority_contract(self, start_contract_date, date_bis):
        if not start_contract_date:
            return ""
        ref_date = date_bis or date.today()
        diff = relativedelta(start_contract_date, ref_date)
        years = abs(diff.years)
        months = abs(diff.months)
        if years:
            return f"{years} year(s) and {months} month(s)"
        return f"{months} month(s)"

    def get_age(self, birth_date, date_bis):
        if not birth_date:
            return 0
        ref_date = date_bis or date.today()
        return ref_date.year - birth_date.year

    def get_spent_monthly_hours(self, monthly_hours):
        if monthly_hours:
            return round((52 * monthly_hours) / 12, 2)
        return 0

    def _get_payslip_lines(self):
        # FIXME: This override re-implements the base _get_payslip_lines to inject
        # custom 'base' and 'nombre' fields. Verify compatibility with v19 payroll API.
        self.ensure_one()

        localdict = self.env.context.get("force_payslip_localdict", None)
        if localdict is None:
            localdict = self._get_localdict()

        rules_dict = localdict["rules"].dict
        result_rules_dict = localdict["result_rules"].dict

        blacklisted_rule_ids = self.env.context.get("prevent_payslip_computation_line_ids", [])
        result = {}
        for rule in sorted(self.struct_id.rule_ids, key=lambda x: x.sequence):
            if rule.id in blacklisted_rule_ids:
                continue
            localdict.update({
                "result": None,
                "result_qty": 1.0,
                "result_rate": 100,
                "result_name": False,
            })
            if rule._satisfy_condition(localdict):
                amount, qty, rate = rule._compute_rule(localdict)
                base = rule._compute_base(localdict)
                nombre = rule._compute_nombre(localdict)
                previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                tot_rule = amount * qty * rate / 100.0
                localdict[rule.code] = tot_rule
                result_rules_dict[rule.code] = {
                    "total": tot_rule,
                    "amount": amount,
                    "quantity": qty,
                }
                rules_dict[rule.code] = rule
                localdict = rule.category_id._sum_salary_rule_category(
                    localdict, tot_rule - previous_amount
                )
                employee_lang = self.employee_id.sudo().address_home_id.lang
                if localdict["result_name"]:
                    rule_name = localdict["result_name"]
                elif rule.code in ("BASIC", "GROSS", "NET", "DEDUCTION", "REIMBURSEMENT"):
                    if rule.code == "BASIC":
                        if rule.name == "Double Holiday Pay":
                            rule_name = _("Double Holiday Pay")
                        elif rule.struct_id.name == "CP200: Employees 13th Month":
                            rule_name = _("Prorated end-of-year bonus")
                        else:
                            rule_name = _("Basic Salary")
                    elif rule.code == "GROSS":
                        rule_name = _("Gross")
                    elif rule.code == "DEDUCTION":
                        rule_name = _("Deduction")
                    elif rule.code == "REIMBURSEMENT":
                        rule_name = _("Reimbursement")
                    elif rule.code == "NET":
                        rule_name = _("Net Salary")
                else:
                    rule_name = rule.with_context(lang=employee_lang).name
                result[rule.code] = {
                    "sequence": rule.sequence,
                    "code": rule.code,
                    "name": rule_name,
                    "note": html2plaintext(rule.note),
                    "salary_rule_id": rule.id,
                    "contract_id": localdict["contract"].id,
                    "employee_id": localdict["employee"].id,
                    "amount": amount,
                    "quantity": qty,
                    "rate": rate,
                    "slip_id": self.id,
                    "base": base or 0.0,
                    "nombre": nombre or 0.0,
                }
        return result.values()
