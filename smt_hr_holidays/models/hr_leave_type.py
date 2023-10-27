# -*- coding: utf-8 -*-

import datetime
import logging

from collections import defaultdict
from datetime import time, timedelta

from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.translate import _
from odoo.tools.float_utils import float_round
from odoo.addons.resource.models.resource import Intervals


class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    is_of_the_paid_leave_type = fields.Boolean()
