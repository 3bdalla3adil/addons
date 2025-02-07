# -*- coding: utf-8 -*-
{
    'name': "Property Management",

    'summary': "Custom Module to Manage Properties AND Maintenance Projects",

    'description': """
     Assuming that Properties are Buildings,
     Vacant land, Compound, Flat, Shop, Store
     and Employees are Officers and Workers ,
     This Module should allow to manage properties for every 
     Property owner and Manage there contracts on there behalf
     and the Property Furnituremanage and maintenance requests""",

    'author': "Eng. Abdulla Bashir",
    'website': "https://www.3bdalla3adil.github.io",
    'category': 'Human Resources',
    'version': '0.1',

    'depends': ['base','hr','account','product','fleet'
                #'maintenance'
                ],

    # always loaded
    'data': [

        #'security/no_claim_deleted.xml',
        'security/ir.model.access.csv',

        'data/details_sequence.xml',

        'views/property_views.xml',

        'views/unit_views.xml',

        'views/pdc_views.xml',
        'views/contract_views.xml',
        'views/move_views.xml',
        'views/invoice_unit.xml',

        'views/owner_views.xml',
        'views/fleet_vehicle_views.xml', # should not be in production

        'views/claim_views.xml',
        # 'views/maintenance_requests.xml',
        'views/claim_type.xml',

        'wizard/claim_request_wizard.xml',

        'report/claim_report.xml',
        'report/claim_report_template.xml',

        'views/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'odoo_property_management/static/src/css/*.css',
        ],
        # 'web._assets_core': [
        # ],
    },
    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

