{
    "name": "smt_contact",
    "summary": "Smarteo Contact — partner extensions (NIF, STAT, RCS, CIF, competitor flag)",
    "description": "Adds Malagasy tax identifiers and competitor flag to res.partner.",
    "author": "NEXOURCES",
    "website": "https://www.nexources.com",
    "category": "Contacts",
    "version": "19.0.1.0.0",
    "depends": ["base", "contacts"],
    "data": [
        "views/res_partner_views.xml",
        "data/ir_cron.xml",
    ],
    "license": "LGPL-3",
}
