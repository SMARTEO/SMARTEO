# -*- coding: utf-8 -*-
{
    'name': "smt_account",
    'summary': "Smarteo Accounting — date_paid on invoices, payment term extensions",
    'description': "Adds payment date computation and payment method field on payment terms.",
    'author': "NEXOURCES",
    'website': "https://www.nexources.com",
    'category': 'Accounting',
    'version': '19.0.1.0.0',
    'depends': ['base', 'smt_base', 'account'],
    'data': [
        'views/account_move_view.xml',
        'views/account_payment_term_views.xml',
        'views/account_move_tree_view.xml',
        'data/ir_cron_data.xml',
    ],
    'license': 'LGPL-3',
}
