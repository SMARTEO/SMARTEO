# -*- coding: utf-8 -*-
{
    "name": "smt_hr_payroll",
    "summary": "Smarteo Payroll — custom payslip fields (base, nombre, leave balances)",
    "author": "NEXOURCES",
    "website": "https://www.nexources.com",
    "category": "Human Resources",
    "version": "19.0.1.0.0",
    "depends": ["base", "hr_payroll", "hr_holidays"],
    "data": [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/base_external_layout.xml",
        "views/hr_payslip.xml",
        "views/payslip_report.xml",
        "views/hr_salary_rule_views.xml",
        "views/hr_payroll_report_views.xml",
    ],
    "license": "LGPL-3",
}
