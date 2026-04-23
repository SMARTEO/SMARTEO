# -*- coding: utf-8 -*-
{
    'name': "softeo_report",
    'summary': "SOFTEO Reports — custom invoice and sale order QWeb templates",
    'author': "NEXOURCES",
    'website': "https://www.nexources.com",
    'category': 'Accounting',
    'version': '19.0.1.0.0',
    'depends': ['sale', 'account'],
    'data': [
        'report/layout_boxed.xml',
        'report/report_invoice.xml',
        'report/report_sale_order.xml',
    ],
    'license': 'LGPL-3',
}
