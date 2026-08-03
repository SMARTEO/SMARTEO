# -*- coding: utf-8 -*-
{
    'name': "alpha_payslip",
    'summary': "Alpha Payslip — custom OWL field widget for payslip display",
    'author': "NEXOURCES",
    'website': "https://www.nexources.com",
    'category': 'Human Resources',
    'version': '19.0.1.0.0',
    'depends': ['base', 'hr', 'hr_payroll'],
    'data': [
        'views/heure_sup.xml',
        'data/data.xml',
    ],
    'license': 'LGPL-3',
    'assets': {
        'web.report_assets_common': [
            'alpha_payslip/static/src/css/bootstrap.css',
        ],
        'web.assets_backend': [
            'alpha_payslip/static/src/css/custom_widget.css',
            'alpha_payslip/static/src/js/custom_widget.js',
            'alpha_payslip/static/src/xml/custom_widget.xml',
        ],
    },
}
