#-*- cofing: utf-8-*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_paid = fields.Date(string='Date of payment', comput="_compute_date_paid", store=True, readonly=False)


    @api.depends("payment_state")
    def _compute_date_paid(self):
        """
        Compute date of paiment
        """
        for move in self:
            if not move.date_paid:
                move.date_paid = fields.Date.today() if move.payment_state == 'paid' else False
            else:
                move.date_paid = move.date_paid