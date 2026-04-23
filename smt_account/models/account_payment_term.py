# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    default_description = fields.Boolean(string='Default Description')
    payment_method = fields.Selection(
        [('transaction', 'Wire Transfer'), ('cash', 'Cash'), ('check', 'Cheque')],
        string='Payment Method',
        default=False,
    )
