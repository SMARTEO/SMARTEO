import logging

from odoo import models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

COMMANDE_ALIAS_NAME = "commande"


class CrmLead(models.Model):
    _inherit = "crm.lead"
    _description = "CRM Lead / Opportunity"

    def _assign_userless_lead_in_team(self, creation_source):
        commande_leads = self.filtered(
            lambda lead: (
                not lead.user_id and lead.team_id.alias_id.alias_name == COMMANDE_ALIAS_NAME
            )
        )
        for lead in commande_leads:
            partner = lead._find_matching_partner()
            if partner and partner.user_id:
                # team_id is computed from user_id and would otherwise drift to the
                # salesperson's own default team if they aren't a member of this one.
                lead.write(
                    {
                        "partner_id": partner.id,
                        "user_id": partner.user_id.id,
                        "team_id": lead.team_id.id,
                    }
                )
                _logger.info(
                    "Lead %s auto-assigned to %s based on matching customer %s",
                    lead.id,
                    partner.user_id.login,
                    partner.name,
                )
                lead._message_log(
                    body=self.env._(
                        "Automatically assigned to %(salesperson)s based on existing "
                        "customer %(partner)s.",
                        salesperson=partner.user_id.name,
                        partner=partner.name,
                    )
                )

        remaining = self - commande_leads
        if remaining:
            super(CrmLead, remaining)._assign_userless_lead_in_team(creation_source)

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
