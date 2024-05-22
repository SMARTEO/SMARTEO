# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    nif = fields.Char()
    stat = fields.Char()
    cif = fields.Char()
    rcs = fields.Char()