# -*- coding: utf-8 -*-
{
    "name": "smt_sale",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "sale", "web", "sale_margin", "sale_management"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/views.xml",
        "views/templates.xml",
        "report/layout_boxed.xml",
        "report/report_invoice.xml",
        "report/report_sale_order.xml",
        "views/sale_order.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "smt_sale/static/src/scss/custom_layout.scss",
        ],
    },
    "demo": [
        "demo/demo.xml",
    ],
}
