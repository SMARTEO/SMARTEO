#-*- cofing: utf-8-*-
import logging
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _move_opportunities_to_lost_stage(self):
        lost_stage_id = self.env['crm.stage'].search([('is_lost', '=', True)], limit=1)
        if not lost_stage_id:
            raise ValidationError(_('No lost stage, this action can not be carried on !'))
        lost_opportunities = self.env['crm.lead'].search([('type', '=', 'opportunity'), ('active', '=', False), ('probability', '=', 0), ('stage_id', '!=', lost_stage_id.id)])
        for lost_opportunity in lost_opportunities:
            logging.info('- {} -'.format(lost_opportunity.id))
            lost_opportunity.write({'stage_id' : lost_stage_id.id})
            self.env.cr.commit()
            logging.info('DONE')
