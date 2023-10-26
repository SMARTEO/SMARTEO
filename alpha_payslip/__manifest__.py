# -*- coding: utf-8 -*-
{
    "name": "alpha_payslip",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "hr", "hr_payroll"],
    # always loaded
    "data": [
        "views/heure_sup.xml",
        "data/data.xml",
    ],
    "license": "LGPL-3",
    "assets": {
        "web.report_assets_common": [
            "alpha_payslip/static/src/css/bootstrap.css",
        ],
        "web.assets_backend": [
            "alpha_payslip/static/src/css/custom_widget.css",
            "alpha_payslip/static/src/js/custom_widget.js",
        ],
        "web.assets_qweb": {
            "alpha_payslip/static/src/xml/custom_widget.xml",
        },
    },
}
