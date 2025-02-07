# -*- coding: utf-8 -*-
{
    'name': "NM - Qatar Contract",

    'summary': """
    This module customizes In-Place the Contracts App by adding new fields (Allowances) to meet the Qatari market needs.
    """,
    'description': """
    This module changes the label of the (contract start date) to (joining date) since the joining date is the base of all calculations. It also adds two new fields (contract signing date) and (contract authenticating date)
    """,
    'author': 'NextMove Business Solutions',
    'website': 'https://www.nextmovebs.com',
    'category': 'HR',
    'version': '1.0',
    'depends': ['base', 'hr_contract'],
    'data': [
        "data/data.xml",
        "views/contract.xml",
    ],
    'license': "Other proprietary",
}
