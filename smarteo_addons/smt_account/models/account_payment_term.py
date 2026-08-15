# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"
    _description = "Payment Term"

    default_description = fields.Boolean(string="Default Description")
    payment_method = fields.Selection(
        [("transaction", "Wire Transfer"), ("cash", "Cash"), ("check", "Cheque")],
        string="Payment Method",
        default=False,
    )
