# -*- coding: utf-8 *-*

from odoo import models, fields

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    default_description = fields.Boolean()
    payment_method = fields.Selection([('transaction', 'transaction'), ('cash', 'cash'), ('check', 'check')], default=False)