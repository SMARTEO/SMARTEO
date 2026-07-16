{
    "name": "smt_sale",
    "summary": "Smarteo Sale — margin tracking, CRM button, order line edit permissions",
    "author": "NEXOURCES",
    "website": "https://www.nexources.com",
    "category": "Sales",
    "version": "19.0.1.0.1",
    "depends": [
        "base",
        "sale",
        "web",
        "sale_margin",
        "sale_management",
        "smt_account",
        "crm",
    ],
    "data": [
        "security/security.xml",
        "views/sale_order.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "smt_sale/static/src/scss/custom_layout.scss",
        ],
    },
    "license": "LGPL-3",
}
