# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'SOFTEO Reports',
    'category': 'Sales/CRM',
    'sequence': 150,
    'summary': 'Centralize your address book',
    'description': """
This module gives you a quick view of your contacts directory, accessible from your home page.
You can track your vendors, customers and other contacts.
""",
    'depends': ['sale','account'],
    'data': [
        # 'report/layout_boxed.xml',
        'report/report_invoice.xml',
        'report/report_sale_order.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
