# -*- encoding: utf-8 -*-
{
    'name': 'Odoo Beauty Clinic Management',
    'version': '17.0',
    'category': 'Services',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'http://pragtech.co.in',

    'depends': ['base', 'mail', 'bus', 'website', 'sale_management', 'purchase', 'product', 'account','repair',
                'attachment_indexation', 'google_calendar', 'product_expiry', 'web', 'calendar'],

    'summary': 'The Beauty clinic management module is very useful for admin and clinics to manage patient'
               ' details, appointments, face marks, body marks, treatment notes, utilized materials,'
               ' generate prescriptions, invoicing and insurance management.',
    'description': """
    This modules includes Beauty Clinic Management Features
    <keywords>
    Odoo - Beauty Clinic Management
    Beauty
    Beauty management app
    Beauty management system
    Beauty management module
    Beauty management 
    odoo Beauty
    Beauty clinic management
    Beauty app
    """,
    "data": [
        'security/dental_security.xml',
        'security/ir.model.access.csv',

        'data/dental_data.xml',
        'data/dental_sequences.xml',
        'data/dose_units.xml',
        'data/medicament_form.xml',
        'data/snomed_frequencies.xml',
        # 'data/occupations.xml',
        # 'data/teeth_code.xml',

        'views/a_view.xml',

        'views/appointment_views.xml',

        'views/patient_views.xml',
        'views/clinic_views.xml',
        'views/doctor_views.xml',

        'views/treatment_views.xml',# nurse pdf forms DONE!

        'views/procedure_views.xml',# remaining DONE!

        'views/equipment_views.xml',# remaining DONE!

        'views/prescription_views.xml',

        # 'views/stock_alert.xml',
        # 'views/alert_data.xml',
        'views/financing_view.xml',
        'views/dental_invoice_view.xml',
        'views/menus.xml',

        'wizard/wizard_actions.xml',
        'wizard/appointment_wizard.xml',
        'wizard/appointment_report_wizard.xml',

        'report/report_claim_form.xml',
        'report/claim_report_temp.xml',
        'report/report_income_by_clinic.xml',
        'report/report_patient_by_clinic.xml',
        'report/report_appointment.xml',
        'report/report_prescription.xml',
        'report/report_prescription_main.xml',
        'report/report_patient_financing_agreement.xml',
        'report/report_income_by_procedure.xml',
        'report/report_patient_by_procedure.xml',
        'report/report_income_by_insurance_company.xml',
        'report/dental_report.xml',

        # 'report/report_daman_reimbursement.xml',
        # 'report/report_oman_reinburstment.xml',
        # 'report/report_nextcare_reimbursement.xml',

        # 'views/my_layout.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'beauty_clinic_management/static/src/xml/*.xml',
            'beauty_clinic_management/static/src/js/*.js',
            'beauty_clinic_management/static/src/css/base_new.css',
        ],
        'web._assets_core': [
            'beauty_clinic_management/static/src/css/select2.min.css',
        ],
    },
    'images': ['images/beauty_clinic_management.gif'],
    'live_test_url': 'http://www.pragtech.co.in/company/proposal-form.html?id=103&name=Odoo-Beauty-Management',
    'license': 'OPL-1',
    'price': 300,
    'currency': 'USD',
    'installable': True,
    'application': True,
    'auto_install': False,
}
