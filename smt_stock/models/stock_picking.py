# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models

class PickingType(models.Model):
    _inherit = "stock.picking.type"

    # def get_stock_picking_action_picking_type(self):
    #     if self.env.user.has_group('smt_stock.group_show_stock_picking_planing'):
    #         return self._get_action('smt_stock.stock_picking_action_picking_type_planing')
    #     else:
    #         return self._get_action('stock.stock_picking_action_picking_type')


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # @api.model
    # def default_get(self, fields):
    #     if self.env.user.has_group('smt_stock.group_show_stock_picking_planing'):
    #         defaults = super(StockPicking, self).default_get(fields)
    #         defaults['planning_issues'] = True
    #     return defaults



