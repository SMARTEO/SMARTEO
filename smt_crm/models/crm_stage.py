# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    is_won = fields.Boolean('Is Won Stage?')
    is_lost = fields.Boolean('Is Lost Stage?', default=False, store=True)

    @api.constrains('is_lost')
    def _check_lost_stage_more_than_one(self):
        for stage in self:
            if stage.is_lost:
                duplicate = self.env['crm.stage'].search([
                    ('is_lost', '=', True),
                    ('id', '!=', stage.id),
                ])
                if duplicate:
                    raise ValidationError(_("There must be only one lost stage!"))
