# -*- coding: utf-8 -*-
{
    "name": "smt_stock",
    "summary": "Smarteo Stock — valuation fields, planning issues view, export button",
    "author": "NEXOURCES",
    "website": "https://www.nexources.com",
    "category": "Inventory",
    "version": "19.0.1.0.0",
    "depends": ["base", "product", "stock", "stock_account"],
    "data": [
        "security/security.xml",
        "views/stock_quant.xml",
        "views/product_product.xml",
        "views/stock_valuation.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_views.xml",
        # 'report/stock_report.xml',
    ],
    "license": "LGPL-3",
}
