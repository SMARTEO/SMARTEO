# -*- coding: utf-8 -*-
{
    'name': "smt_crm",
    'summary': "CRM — move lost opportunities to the lost stage",
    'description': "Scheduled action to move all lost opportunities into the 'Lost stage'.",
    'author': "NEXOURCES",
    'website': "https://www.nexources.com",
    'category': 'CRM',
    'version': '19.0.1.0.0',
    'depends': ['base', 'smt_base', 'crm'],
    'data': [
        'data/ir_cron.xml',
        'views/crm_stage_views.xml',
        'i18n/fr.po',
    ],
    'license': 'LGPL-3',
}
