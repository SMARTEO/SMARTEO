import logging

from odoo import models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"
    _description = "CRM Lead / Opportunity"

    def _move_opportunities_to_lost_stage(self):
        lost_stage = self.env["crm.stage"].search([("is_lost", "=", True)], limit=1)
        if not lost_stage:
            raise ValidationError(self.env._("No lost stage — this action cannot be carried on!"))
        lost_opportunities = self.env["crm.lead"].search(
            [
                ("active", "=", False),
                ("probability", "=", 0),
                ("stage_id", "!=", lost_stage.id),
            ]
        )
        for opportunity in lost_opportunities:
            _logger.info(
                "Moving opportunity %s (stage %s) to lost stage",
                opportunity.id,
                opportunity.stage_id.id,
            )
            opportunity.write({"stage_id": lost_stage.id})
            _logger.info(
                "Done — opportunity %s now in stage %s", opportunity.id, opportunity.stage_id.id
            )
