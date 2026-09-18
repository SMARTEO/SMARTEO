import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Contact"

    nif = fields.Char("NIF")
    stat = fields.Char("STAT")
    rcs = fields.Char("RCS")
    cif = fields.Char("CIF")
    customer = fields.Boolean("Customer")
    supplier = fields.Boolean("Supplier")
    compete = fields.Boolean("Competitor")
    phone1 = fields.Char()
    phone2 = fields.Char()
    phone3 = fields.Char()
    can_edit_payment_terms = fields.Boolean(
        string="May change the payment terms",
        compute="_compute_can_edit_payment_terms",
    )

    @api.depends_context("uid")
    def _compute_can_edit_payment_terms(self):
        can_edit = self.env.user.has_group("smt_base.group_can_edit_payment_terms")
        for partner in self:
            partner.can_edit_payment_terms = can_edit

    def update_compete_for_child(self):
        partners = self.search([("compete", "=", True)])
        for rec in partners:
            for child in rec.child_ids:
                child.compete = True

    @api.onchange("compete")
    def _onchange_compete(self):
        for rec in self:
            if rec.compete:
                rec.child_ids.write({"compete": True})
