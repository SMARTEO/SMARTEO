from odoo import api, fields, models, _


class StockQuant(models.Model):
    _inherit = "stock.quant"

    standard_price = fields.Float(
        related="product_id.standard_price",
        string="Prix unitaire",
        readonly=True,
        store=True,
        group_operator="avg",
    )
    values = fields.Float(compute="_compute_values", string="Valeur total", store=True)

    @api.depends("inventory_quantity_auto_apply", "standard_price")
    def _compute_values(self):
        for record in self:
            record.values = record.inventory_quantity_auto_apply * record.standard_price
