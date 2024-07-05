# -*- coding:utf-8 -*-


from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import html2plaintext


class HrPayslip(models.Model):
	_inherit = "hr.payslip"
	
	commentaire = fields.Text(string="Commentaire", required=False)
	
	paid_date = fields.Date(string="Date de paie ", required=False, readonly=True)
	is_balance_all_account = fields.Boolean()
	# balance_to_date = fields.Float(compute='_get_remaining_leaves', store=True)
	balance_to_date = fields.Float()
	gain_on_current_month = fields.Selection([('0', '0'), ('2.5', '2,5')], default='2.5')
	# balance_on_pay_slip = fields.Float(compute='_get_balance_remaining_leaves', store=True)
	balance_on_pay_slip = fields.Float()
	payment_method_in_pdf = fields.Char()
	is_can_modif_all_balance = fields.Boolean(compute='_compute_is_can_modif_all_balance')
	# previous_paid_leave_balance = fields.Float()
	previous_paid_leave_balance = fields.Float(compute="compute_previous_paid_leave_balance", store=True,
	                                           readonly=False)
	days_taken_in_the_month = fields.Float(compute='compute_days_taken_in_the_month')
	new_balance_in_the_month = fields.Float(compute='_compute_new_balance_in_the_month')
	
	def _compute_is_can_modif_all_balance(self):
		if self.env.user.has_group('smt_hr_payroll.group_can_modif_balance_payroll'):
			self.is_can_modif_all_balance = True
		else:
			self.is_can_modif_all_balance = False
	
	@api.model_create_multi
	def create(self, vals_list):
		res = super(HrPayslip, self).create(vals_list)
		for payslip in res:
			if payslip.employee_id and payslip.gain_on_current_month:
				payslip.balance_to_date = payslip.employee_id.leaves_count
				if payslip.gain_on_current_month == '2.5':
					payslip.balance_on_pay_slip = payslip.employee_id.leaves_count + 2.5
				else:
					payslip.balance_on_pay_slip = payslip.employee_id.leaves_count
		return res
	
	def write(self, vals):
		res = super(HrPayslip, self).write(vals)
		if 'gain_on_current_month' in vals and vals['gain_on_current_month']:
			for slip in self:
				if vals['gain_on_current_month'] == '2.5':
					slip.balance_on_pay_slip = slip.balance_to_date + 2.5
				else:
					slip.balance_on_pay_slip = slip.balance_to_date
		return res
	
	# @api.onchange('employee_id')
	# def set_balance_onchange_date(self):
	#     if self.env.user.has_group('smt_hr_payroll.group_can_modif_balance_payroll'):
	#         self.is_can_modif_all_balance = True
	#     else:
	#         self.is_can_modif_all_balance = False
	#     for paye in self:
	#         if paye.employee_id:
	#             # last_payroll = self.env['hr.payslip'].search([
	#             #     ('employee_id', '=', paye.employee_id.id),
	#             # ], order='date_to desc', limit=1)
	#             #
	#             # if last_payroll:
	#             #     paye.previous_paid_leave_balance = last_payroll.new_balance_in_the_month
	#             # else:
	#             #     paye.previous_paid_leave_balance = 0.0
	#             holiday_status_id = self.env.ref('hr_holidays.holiday_status_cl')
	#             allocation = self.env['hr.leave.allocation'].search(
	#                 [('state', '=', 'validate'), ('holiday_status_id', '=', holiday_status_id.id),
	#                  ('date_from', '<=', paye.date_from), ('employee_id', '=', paye.employee_id.id)])
	#             accrual_ids = allocation.mapped('accrual_plan_id')
	#             levels = self.env['hr.leave.accrual.level'].search([('accrual_plan_id', 'in', accrual_ids.ids)])
	#             paye.previous_paid_leave_balance = sum(levels.mapped('added_value'))
	# paye.days_taken_in_the_month = sum(paye.worked_days_line_ids.filtered(lambda w: w.work_entry_type_id.code == 'LEAVE100').mapped('number_of_days'))
	
	def compute_days_taken_in_the_month(self):
		for paye in self:
			paye.days_taken_in_the_month = sum(
				paye.worked_days_line_ids.filtered(lambda w: w.work_entry_type_id.code == 'LEAVE100').mapped(
					'number_of_days'))
	
	@api.onchange('previous_paid_leave_balance')
	def onchange_previous_paid_leave_balance(self):
		for paye in self:
			paye.new_balance_in_the_month = (paye.previous_paid_leave_balance + float(
				paye.gain_on_current_month)) - paye.days_taken_in_the_month
	
	def _compute_new_balance_in_the_month(self):
		for paye in self:
			paye.new_balance_in_the_month = (paye.previous_paid_leave_balance + float(
				paye.gain_on_current_month)) - paye.days_taken_in_the_month
	
	def calculate_cumul_leaves(self, date):
		holiday_status_id = self.env.ref('hr_holidays.holiday_status_cl')
		leaves = self.env['hr.leave'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'validate'),
		                                      ('holiday_status_id', '=', holiday_status_id.id),
		                                      ('request_date_from', '<', date),
		                                      ('request_date_to', '<=', date)])
		return sum(leaves.mapped('number_of_days'))
	
	def calculate_cumul_allocation(self, date):
		holiday_status_id = self.env.ref('hr_holidays.holiday_status_cl')
		allocation_regulars = self.env['hr.leave.allocation'].search(
			[('state', '=', 'validate'), ('allocation_type', '=', 'regular'),
			 ('holiday_status_id', '=', holiday_status_id.id)
				, ('employee_id', '=', self.employee_id.id),
             ('date_from', '<=', date), '|', ('date_to', '>=', date), ('date_to', '=', False)])
		allocation_accruals = self.env['hr.leave.allocation'].search(
			[('state', '=', 'validate'), ('allocation_type', '=', 'accrual'),
			 ('holiday_status_id', '=', holiday_status_id.id),
			 ('employee_id', '=', self.employee_id.id),
			 ('date_from', '<=', date), '|', ('date_to', '>=', date), ('date_to', '=', False)])
		level_value = 0.00
		for allocation_accrual in allocation_accruals:
			accrual_id = allocation_accrual.accrual_plan_id
			levels = self.env['hr.leave.accrual.level'].search([('accrual_plan_id', '=', accrual_id.id)])
			for level in levels:
				if level.frequency == 'daily':
					coef = relativedelta(self.date_from,allocation_accrual.date_from).days
				if level.frequency == 'weekly':
					coef = relativedelta(self.date_from,allocation_accrual.date_from).days / 7
				if level.frequency == 'bimonthly':
					coef = relativedelta(self.date_from,allocation_accrual.date_from).months / 2
				if level.frequency == 'monthly':
					diff_years = relativedelta(self.date_from,allocation_accrual.date_from).years
					diff_monts = relativedelta(self.date_from,allocation_accrual.date_from).months
					diff_days = relativedelta(self.date_from,allocation_accrual.date_from).days
					coef = diff_years * 12 + diff_monts + (diff_days/ 30)
				if level.frequency == 'biyearly':
					coef = relativedelta(self.date_from,allocation_accrual.date_from).years / 2
				if level.frequency == 'yearly':
					coef = relativedelta(self.date_from,allocation_accrual.date_from).years
				value = level.added_value * coef if level.added_value_type == 'days' else level.added_value * coef / 24
				level_value += value if level.maximum_leave >= value else level.maximum_leave
		final_value = level_value + sum(allocation_regulars.mapped('number_of_days'))
		return final_value
	
	@api.depends('employee_id', 'date_from')
	def compute_previous_paid_leave_balance(self):
		for payslip in self:
			payslip.previous_paid_leave_balance = 0.00
			if payslip.employee_id:
				payslip.previous_paid_leave_balance = payslip.calculate_cumul_allocation(
					payslip.date_from) - payslip.calculate_cumul_leaves(payslip.date_from)
	
	def refresh_payslip_leave_situation(self):
		self.compute_days_taken_in_the_month()
		self._compute_new_balance_in_the_month()
		self.compute_previous_paid_leave_balance()
	
	# def _get_remaining_leaves(self):
	#     for paye in self:
	#         paye.balance_to_date = paye.employee_id.leaves_count
	
	# def _get_balance_remaining_leaves(self):
	#     for paye in self:
	#         if paye.gain_on_current_month == "2":
	#             paye.balance_on_pay_slip = paye.balance_to_date + 2.5
	#         elif paye.gain_on_current_month == "0":
	#             paye.balance_on_pay_slip = paye.balance_to_date
	
	@api.onchange('employee_id')
	def get_balance_to_date(self):
		for paye in self:
			paye.balance_to_date = paye.employee_id.leaves_count
			if paye.gain_on_current_month == "2.5":
				paye.balance_on_pay_slip = paye.balance_to_date + 2.5
			elif paye.gain_on_current_month == "0":
				paye.balance_on_pay_slip = paye.balance_to_date
	
	@api.onchange('gain_on_current_month', 'employee_id')
	def change_gain_on_current_month(self):
		for paye in self:
			if paye.gain_on_current_month == "2.5":
				paye.balance_on_pay_slip = paye.balance_to_date + 2.5
			elif paye.gain_on_current_month == "0":
				paye.balance_on_pay_slip = paye.balance_to_date
	
	def compute_sheet(self):
		payslips = self.filtered(lambda slip: slip.state in ["draft", "verify"])
		# delete old payslip lines
		payslips.line_ids.unlink()
		for payslip in payslips:
			number = payslip.number or self.env["ir.sequence"].next_by_code(
				"salary.slip"
			)
			lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
			payslip.write(
				{
					"line_ids": lines,
					"number": number,
					"state": "verify",
					"compute_date": fields.Date.today(),
				}
			)
		self.paid_date = datetime.now()
		return True
	
	def get_seniority_contract(self, start_contract_date, date_bis):
		years_months = ""
		if start_contract_date:
			today = date.today()
			if date_bis:
				diff_date = relativedelta(start_contract_date, date_bis)
				if diff_date.years != 0:
					years_months = str(diff_date.years).replace('-', '') + ' ans et ' + str(diff_date.months).replace(
						'-', '') + ' mois'
				else:
					years_months = str(diff_date.months).replace('-', '') + ' mois'
			else:
				diff_date_today = relativedelta(start_contract_date, today)
				if diff_date_today.years != 0:
					years_months = str(diff_date_today.years).replace('-', '') + ' ans et ' + str(
						diff_date_today.months).replace('-', '') + ' mois'
				else:
					years_months = str(diff_date_today.months).replace('-', '') + ' mois'
		return years_months
	
	def get_age(self, birth_date, date_bis):
		age = 0
		if birth_date:
			today = date.today()
			
			if date_bis:
				end_date = date_bis
				age = end_date.year - birth_date.year
			
			else:
				age = today.year - birth_date.year
		
		return age
	
	def get_spent_monthly_hours(self, monthly_hours):
		if monthly_hours:
			spent_hours = round(((52 * monthly_hours) / 12), 2)
			return spent_hours
	
	def _get_payslip_lines(self):
		self.ensure_one()
		
		localdict = self.env.context.get("force_payslip_localdict", None)
		if localdict is None:
			localdict = self._get_localdict()
		
		rules_dict = localdict["rules"].dict
		result_rules_dict = localdict["result_rules"].dict
		
		blacklisted_rule_ids = self.env.context.get(
			"prevent_payslip_computation_line_ids", []
		)
		result = {}
		for rule in sorted(self.struct_id.rule_ids, key=lambda x: x.sequence):
			if rule.id in blacklisted_rule_ids:
				continue
			localdict.update(
				{
					"result": None,
					"result_qty": 1.0,
					"result_rate": 100,
					"result_name": False,
				}
			)
			if rule._satisfy_condition(localdict):
				amount, qty, rate = rule._compute_rule(localdict)
				base = rule._compute_base(localdict)
				nombre = rule._compute_nombre(localdict)
				# check if there is already a rule computed with that code
				previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
				# set/overwrite the amount computed for this rule in the localdict
				tot_rule = amount * qty * rate / 100.0
				localdict[rule.code] = tot_rule
				result_rules_dict[rule.code] = {
					"total": tot_rule,
					"amount": amount,
					"quantity": qty,
				}
				rules_dict[rule.code] = rule
				# sum the amount for its salary category
				localdict = rule.category_id._sum_salary_rule_category(
					localdict, tot_rule - previous_amount
				)
				# Retrieve the line name in the employee's lang
				employee_lang = self.employee_id.sudo().address_home_id.lang
				# This actually has an impact, don't remove this line
				context = {"lang": employee_lang}
				if localdict["result_name"]:
					rule_name = localdict["result_name"]
				elif rule.code in [
					"BASIC",
					"GROSS",
					"NET",
					"DEDUCTION",
					"REIMBURSEMENT",
				]:  # Generated by default_get (no xmlid)
					if (
							rule.code == "BASIC"
					):  # Note: Crappy way to code this, but _(foo) is forbidden. Make a method in master to be overridden, using the structure code
						if rule.name == "Double Holiday Pay":
							rule_name = _("Double Holiday Pay")
						if rule.struct_id.name == "CP200: Employees 13th Month":
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
				# create/overwrite the rule in the temporary results
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
					"base": base,
					"nombre": nombre,
				}
		
		return result.values()
