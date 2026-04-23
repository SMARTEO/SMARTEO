# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock MTS+MTO Rule",
    "summary": "Add a MTS+MTO route",
    # REPLACE THIS ENTIRE MODULE with the OCA v19 release:
    # pip install git+https://github.com/OCA/stock-logistics-warehouse@19.0#subdirectory=stock_mts_mto_rule
    "version": "19.0.1.0.1",
    "development_status": "Mature",
    "category": "Warehouse",
    "website": "https://github.com/OCA/stock-logistics-warehouse",
    "author": "Akretion,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock"],
    "data": ["data/stock_data.xml", "view/pull_rule.xml", "view/warehouse.xml"],

}
