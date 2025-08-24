#-*- cofing: utf-8-*-
import logging
from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _move_opportunities_to_lost_stage(self):
        lost_stage_id = self.env['crm.stage'].search([('is_lost', '=', True)], limit=1)
        lost_opportunities = self.env['crm.lead'].search([('type', '=', 'opportunity'), ('active', '=', False), ('probability', '=', 0), ('stage_id', '!=', lost_stage_id.id)])
        for lost_opportunity in lost_opportunities:
            lost_opportunity.write({'stage_id' : lost_stage_id.id})