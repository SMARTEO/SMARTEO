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
