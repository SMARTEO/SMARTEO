# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    nif = fields.Char('NIF')
    stat = fields.Char('STAT')
    rcs = fields.Char('RCS')
    cif = fields.Char('CIF')
    customer = fields.Boolean('Client')
    supplier = fields.Boolean('Fournisseur')
    compete = fields.Boolean('Concurrent')


    def update_compete_for_child(self):
        partner = self.search([('compete', '=', True)])
        for rec in partner:
            for child in rec.child_ids:
                child.compete = True

    @api.onchange('compete')
    def _onchange_compete(self):
        """Quand on change compete dans le formulaire, on répercute sur les enfants."""
        for rec in self:
            if rec.compete:
                rec.child_ids.write({'compete': True})
