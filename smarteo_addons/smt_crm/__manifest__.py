{
    "name": "smt_crm",
    "summary": "CRM — lost opportunity handling and email-lead auto-assignment",
    "description": (
        "Scheduled action to move all lost opportunities into the 'Lost stage'. "
        "Also auto-assigns leads created from the 'commande' mail alias to the "
        "salesperson of the matching existing customer, if any."
    ),
    "author": "NEXOURCES",
    "website": "https://www.nexources.com",
    "category": "CRM",
    "version": "19.0.1.0.0",
    "depends": ["base", "smt_base", "crm"],
    "data": [
        "data/ir_cron.xml",
        "views/crm_stage_views.xml",
    ],
    "license": "LGPL-3",
}
