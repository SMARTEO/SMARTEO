#-*- cofing: utf-8-*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    is_won = fields.Boolean('Is Won Stage?')
    is_lost = fields.Boolean('Is Lost Stage?', default=False, store=True)

    @api.constrains('is_lost')
    def _check_lost_stage_more_than_one(self):
        for comp in self:
            lost_stage = self.env['crm.stage'].search([('is_lost', '=', True), ('id', '!=', comp.id)])
            if comp.is_lost:
                if lost_stage:
                    raise ValidationError(_("There has to be only one lost stage !"))