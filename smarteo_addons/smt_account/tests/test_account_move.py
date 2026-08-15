# -*- coding: utf-8 -*-
from odoo import fields
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestAccountMoveDatePaid(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Date Paid Customer'})
        cls.bank_journal = cls.env['account.journal'].search([('type', '=', 'bank')], limit=1)
        income_account = cls.env['account.account'].search([
            ('account_type', '=', 'income'),
        ], limit=1)
        cls.invoice = cls.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': cls.partner.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': 'Service',
                'quantity': 1,
                'price_unit': 100.0,
                'account_id': income_account.id,
            })],
        })

    def test_date_paid_false_on_draft_invoice(self):
        self.assertFalse(self.invoice.date_paid)

    def test_date_paid_false_when_posted_but_not_paid(self):
        self.invoice.action_post()

        self.assertEqual(self.invoice.payment_state, 'not_paid')
        self.assertFalse(self.invoice.date_paid)

    def test_date_paid_set_when_invoice_fully_paid(self):
        self.invoice.action_post()
        payment_date = fields.Date.today()
        payment = self.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': self.partner.id,
            'amount': self.invoice.amount_total,
            'date': payment_date,
            'journal_id': self.bank_journal.id,
        })
        payment.action_post()

        receivable_lines = (self.invoice.line_ids | payment.move_id.line_ids).filtered(
            lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled
        )
        receivable_lines.reconcile()

        self.assertEqual(self.invoice.payment_state, 'paid')
        self.assertEqual(self.invoice.date_paid, payment_date)

    def test_compute_old_paid_invoice_dates_backfills_missing_date(self):
        self.invoice.action_post()
        payment_date = fields.Date.today()
        payment = self.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'partner_id': self.partner.id,
            'amount': self.invoice.amount_total,
            'date': payment_date,
            'journal_id': self.bank_journal.id,
        })
        payment.action_post()
        receivable_lines = (self.invoice.line_ids | payment.move_id.line_ids).filtered(
            lambda l: l.account_id.account_type == 'asset_receivable' and not l.reconciled
        )
        receivable_lines.reconcile()
        self.assertTrue(self.invoice.date_paid)
        # Simulate a legacy invoice whose date_paid was never backfilled.
        self.invoice.date_paid = False

        self.env['account.move']._compute_old_paid_invoice_dates()

        self.assertEqual(self.invoice.date_paid, payment_date)
