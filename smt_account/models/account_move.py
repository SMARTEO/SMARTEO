#-*- cofing: utf-8-*-
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_paid = fields.Date(string='Date of payment', compute="_compute_date_paid", store=True, readonly=False)


    @api.depends('payment_state', 'state', 'to_check')
    def _compute_date_paid(self):
        """
        Compute date of paiment
        """
        for move in self:
            if move.state != 'posted' or move.payment_state not in ['paid', 'in_payment', 'partial', 'reversed']:
                move.date_paid = False
                continue

            if not move.date_paid:
                lignes = move.line_ids.filtered(lambda l: l.account_internal_type in ['receivable', 'payable'])
                paiements = (
                    lignes.mapped('matched_debit_ids.debit_move_id.payment_id') | 
                    lignes.mapped('matched_credit_ids.credit_move_id.payment_id')
                ).filtered(lambda p: p.date)

                paiement_other = (
                    lignes.mapped('matched_debit_ids.debit_move_id') | 
                    lignes.mapped('matched_credit_ids.credit_move_id')
                ).filtered(lambda p: p.date)

                p = paiements or paiement_other
                
                if p:
                    latest_date =  max(p.mapped('date'))
                    move.date_paid = latest_date
                else:
                    move.date_paid = False
            else:
                move.date_paid = move.date_paid
    
    @api.model
    def _compute_old_paid_invoice_dates(self):
        """
        Compute date paid For all passed invoices
        """
        domain = [
            ('state', '=', 'posted'),
            ('payment_state', 'in', ['paid', 'in_payment', 'partial']),
            ('date_paid', '=', False),
            ('move_type', 'in', ['out_invoice', 'in_invoice']),
        ]
        moves = self.search(domain, limit=3000)

        for move in moves:
            if move.state != 'posted' or move.payment_state not in ['paid', 'in_payment', 'partial', 'reversed']:
                move.date_paid = False
                continue

            lines = move.line_ids.filtered(lambda l: l.account_internal_type in ('receivable', 'payable'))

            payments = (
                lines.mapped('matched_debit_ids.debit_move_id.payment_id') |
                lines.mapped('matched_credit_ids.credit_move_id.payment_id')
            ).filtered(lambda p: p and p.date)

            paiement_other = (
                lines.mapped('matched_debit_ids.debit_move_id') | 
                lines.mapped('matched_credit_ids.credit_move_id')
                ).filtered(lambda m: m.date)

            p = payments or paiement_other
            if p:
                latest_date =  max(p.mapped('date'))
                move.date_paid = move.date_paid or latest_date
            else:
                move.date_paid = move.date_paid or False
