# -*- coding: utf-8 -*-
{
    'name': "SOFTEO-REPORTS",

    'summary': """
        SOFTEO - SALE""",

    'description': """
        SOFTEO report sale
    """,
 
    'author': "Nexources",
    'website': "http://www.nexources.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','account','sale','sale_management'],

  
    'data': [
        'report/report_invoice_inherit.xml',
        'report/report_sale_order_inherit.xml',
        'report/action_inherit.xml',
    ],
}
