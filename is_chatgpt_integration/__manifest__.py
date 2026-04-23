# -*- coding: utf-8 -*-
{
    'name': 'Odoo ChatGPT Integration',
    'version': '19.0.1.0.0',
    'summary': 'Odoo ChatGPT Integration',
    'description': (
        'Allows the application to leverage the capabilities of the GPT language model '
        'to generate human-like responses in the Discuss module.'
    ),
    'author': 'InTechual Solutions / NEXOURCES',
    'website': 'https://www.nexources.com',
    'category': 'Discuss',
    'depends': ['base', 'base_setup', 'mail', 'discuss'],
    'data': [
        'data/mail_channel_data.xml',
        'data/user_partner_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {'python': ['openai']},
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
