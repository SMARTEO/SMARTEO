# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    nif = fields.Char('NIF')
    stat = fields.Char('STAT')
    rcs = fields.Char('RCS')
    cif = fields.Char('CIF')
    customer = fields.Boolean('Customer')
    supplier = fields.Boolean('Supplier')
    compete = fields.Boolean('Competitor')

    def update_compete_for_child(self):
        partners = self.search([('compete', '=', True)])
        for rec in partners:
            for child in rec.child_ids:
                child.compete = True

    @api.onchange('compete')
    def _onchange_compete(self):
        for rec in self:
            if rec.compete:
                rec.child_ids.write({'compete': True})
