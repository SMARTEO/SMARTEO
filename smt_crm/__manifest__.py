# -*- coding: utf-8 -*-
{
    'name': "smt_crm",

    'summary': """ CRM - Lost opportunities """,

    'description': """
        Scheduled action to move all lost opportunities into the "Lost stage"
    """,

    'author': "NEXOURCES - Henintsoa Moria aka Pops",
    'website': "http://www.nexources.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'smt_base', 'crm'],

    # always loaded
    'data': [
        'data/ir_cron.xml',
        'views/crm_stage_views.xml',
    ],
    'license': 'LGPL-3',
}
