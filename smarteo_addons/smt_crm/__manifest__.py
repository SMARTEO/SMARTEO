{
    "name": "smt_crm",
    "summary": "CRM — lost opportunity handling and per-user stage visibility",
    "description": (
        "Scheduled action to move all lost opportunities into the 'Lost stage'. "
        "Also allows restricting specific users from seeing a given stage "
        "and its leads/opportunities."
    ),
    "author": "NEXOURCES",
    "website": "https://www.nexources.com",
    "category": "CRM",
    "version": "19.0.1.0.0",
    "depends": ["base", "smt_base", "crm"],
    "data": [
        "security/crm_security.xml",
        "data/ir_cron.xml",
        "views/crm_lead_views.xml",
        "views/crm_stage_views.xml",
    ],
    "license": "LGPL-3",
}
