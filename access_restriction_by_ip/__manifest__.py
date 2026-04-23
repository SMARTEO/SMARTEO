# -*- coding: utf-8 -*-
{
    'name': 'Access Restriction By IP',
    'summary': "Restrict user login to specified IP addresses",
    'version': '19.0.1.0.0',
    'author': 'Cybrosys Techno Solutions / NEXOURCES',
    'website': 'https://www.nexources.com',
    'category': 'Tools',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/allowed_ips_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
