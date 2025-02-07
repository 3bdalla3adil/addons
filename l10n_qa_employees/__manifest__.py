# -*- coding: utf-8 -*-
{
    'name': "NM - Qatar Employee",
    
    'summary': "This module customizes In-Place the Employees App by adding new fields and functionality to meet the Qatari market needs.",
    'version': '1.0',
    'category': 'Human Resources',
    'author': 'NextMove Business Solutions',
    'website': 'https://www.nextmovebs.com',
    'depends': ['base', 'hr'],
    'data': [
        "security/ir.model.access.csv",
        "data/access_rights.xml",
        "data/insurance_sate.xml",
        "data/schedule.xml",
        "views/hr_employee_views.xml",
        "views/res_config.xml",
        "views/hr_dependants_views.xml",
        "views/hr_insurance_views.xml",
        'views/res_company.xml'
    ],
    'license': 'LGPL-3',
}
