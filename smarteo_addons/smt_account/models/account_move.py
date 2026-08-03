# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Journal Entry'

    date_paid = fields.Date(
        string='Date of Payment',
        compute='_compute_date_paid',
        store=True,
        readonly=False,
    )

    @api.depends('payment_state', 'state')
    def _compute_date_paid(self):
        for move in self:
            if move.state != 'posted' or move.payment_state not in ('paid', 'in_payment', 'partial', 'reversed'):
                move.date_paid = False
                continue

            if not move.date_paid:
                # In v17+ account_internal_type was removed; use account_type instead.
                lines = move.line_ids.filtered(
                    lambda l: l.account_id.account_type in ('asset_receivable', 'liability_payable')
                )
                payments = (
                    lines.mapped('matched_debit_ids.debit_move_id.payment_id') |
                    lines.mapped('matched_credit_ids.credit_move_id.payment_id')
                ).filtered(lambda p: p.date)

                other_moves = (
                    lines.mapped('matched_debit_ids.debit_move_id') |
                    lines.mapped('matched_credit_ids.credit_move_id')
                ).filtered(lambda m: m.date)

                candidates = payments or other_moves
                move.date_paid = max(candidates.mapped('date')) if candidates else False
            else:
                move.date_paid = move.date_paid

    @api.model
    def _compute_old_paid_invoice_dates(self):
        domain = [
            ('state', '=', 'posted'),
            ('payment_state', 'in', ['paid', 'in_payment', 'partial']),
            ('date_paid', '=', False),
            ('move_type', 'in', ['out_invoice', 'in_invoice']),
        ]
        moves = self.search(domain, limit=3000)
        for move in moves:
            if move.state != 'posted' or move.payment_state not in ('paid', 'in_payment', 'partial', 'reversed'):
                move.date_paid = False
                continue

            lines = move.line_ids.filtered(
                lambda l: l.account_id.account_type in ('asset_receivable', 'liability_payable')
            )
            payments = (
                lines.mapped('matched_debit_ids.debit_move_id.payment_id') |
                lines.mapped('matched_credit_ids.credit_move_id.payment_id')
            ).filtered(lambda p: p and p.date)

            other_moves = (
                lines.mapped('matched_debit_ids.debit_move_id') |
                lines.mapped('matched_credit_ids.credit_move_id')
            ).filtered(lambda m: m.date)

            candidates = payments or other_moves
            if candidates:
                move.date_paid = move.date_paid or max(candidates.mapped('date'))
            else:
                move.date_paid = move.date_paid or False
