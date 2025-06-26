# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Ext",
    "summary": """
        attach in order line and open in odoo18 spreadsheet""",
    "version": "14.0.0.1",
    "license": "AGPL-3",
    "author": "NHS",
    "website": "https://github.com/NayHtetSann",
    "depends": ["base", "sale"],
    "data": [
        "views/order_line_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ],
}
