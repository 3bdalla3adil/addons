# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    passport_expiry_date = fields.Date("Passport Expiry Date", groups="hr.group_hr_user")
    passport_last_notification_date = fields.Date("Passport Last Notification Date", groups="hr.group_hr_user")
    qid = fields.Char("QID", help="Qatari ID", groups="hr.group_hr_user")
    driving_license_number = fields.Char("Driving License Number", groups="hr.group_hr_user")
    qid_expiry_date = fields.Date("QID Expiry Date", help="Qatari ID Expiry Date", groups="hr.group_hr_user")
    qid_last_notification_date = fields.Date("QID Last Notification Date", help="Qatari ID Last Notification Date",
                                             groups="hr.group_hr_user")
    driving_license_issuing_date = fields.Date("Driving License Issuing Date", groups="hr.group_hr_user")
    driving_license_expiry_date = fields.Date("Driving License Expiry Date", groups="hr.group_hr_user")
    driving_license_last_notification_date = fields.Date("Driving License Last Notification Date",
                                                         groups="hr.group_hr_user")
    health_care_card_no = fields.Char("Health Care Card No.", groups="hr.group_hr_user")
    health_care_card_expiry_date = fields.Date("Health Care Card Expiry date", groups="hr.group_hr_user")
    health_care_card_last_notification_date = fields.Date("Health Care Card Last Notification Date",
                                                          groups="hr.group_hr_user")
    blood_group = fields.Char("Blood Group", groups="hr.group_hr_user")
    dependants_ids = fields.One2many('hr.dependants', 'employee_id', string='Dependants')
    insure_ids = fields.One2many('hr.insurance.qa', 'employee_id', string='Insurances')

    @api.constrains('qid')
    def _constrains_qid(self):
        for rec in self.filtered(lambda x: x.qid != False):
            same_qid = self.search(
                [('qid', '=', rec.qid), ('id', '!=', rec.id), ('company_id', '=', self.env.user.company_id.id)])
            if same_qid:
                raise ValidationError(_("QID must be unique per employee."))
            if len(rec.qid) != 11:
                raise ValidationError(_("QID must contain 11 character."))

    def send_documents_expiry_email(self):
        lagally_to_renotify = fields.Date.today() + timedelta(days=14)
        soon_expiry_date = fields.Date.today() + timedelta(days=30)
        company = self.env['res.company'].sudo().search([])
        for res in company:
            qid_expire_soon = self.sudo().search(['&', ("qid_expiry_date", "<=", soon_expiry_date), '|',
                                        ("qid_last_notification_date", ">", lagally_to_renotify),
                                        ("qid_last_notification_date", "=", False),
                                        ('company_id', '=', res.id)])
            driving_license_expire_soon = self.sudo().search(['&', ("driving_license_expiry_date", "<=", soon_expiry_date), '|',
                                                ("driving_license_last_notification_date", ">", lagally_to_renotify),
                                                ("driving_license_last_notification_date", "=", False),
                                                ('company_id', '=', res.id)])
            health_care_card_expire_soon = self.sudo().search(['&', ("health_care_card_expiry_date", "<=", soon_expiry_date), '|',
                                                ("health_care_card_last_notification_date", ">",lagally_to_renotify),
                                                ("health_care_card_last_notification_date", "=", False),
                                                ('company_id', '=', res.id)])
            passport_expire_soon = self.sudo().search(['&', ("passport_expiry_date", "<=", soon_expiry_date), '|',
                                        ("passport_last_notification_date", ">", lagally_to_renotify),
                                        ("passport_last_notification_date", "=", False), 
                                        ('company_id', '=', res.id)])
            if qid_expire_soon or driving_license_expire_soon or health_care_card_expire_soon or passport_expire_soon:
                body = """<!DOCTYPE html><html><head><style>table, th, td {
                                border: 1px solid black;
                                border-collapse: collapse;
                            }
                            td{
                            width:200px;
                            }
                            </style></head><body>
                            <img src="/l10n_qa_employees/static/src/img/logo.jpeg"
                            """
                body += '<div style="direction:ltr"></br><h2  style="font-size:17px;text-align:center;">Documents will expire soon</h2> '
                if passport_expire_soon:
                    body += """
                    <p>Passports will expire soon</p>
                    <table class="tb1 table table-sm o_main_table">
                                        <tr>
                                            <th >Employee Name</th>
                                            <th >Passport Number</th>
                                            <th >Passport Expiry Date</th>
                                            <th >Employee Company</th>
                                    </tr>"""

                    for passport_employee in passport_expire_soon:
                        body += """<tr>  
                                    <td>{}</td>
                                    <td>{}</td>
                                    <td >{}</td>
                                    <td >{}</td>
                                    </tr>
                                """.format(passport_employee.name, passport_employee.passport_id,
                                            passport_employee.passport_expiry_date,passport_employee.company_id.name)
                        passport_employee.passport_last_notification_date = fields.Date.today()
                    body += """</table> <br/> <br/> <br/>"""

                if qid_expire_soon:
                    body += """
                    <p>QID will expire soon</p>
                    <table class="tb1 table table-sm o_main_table">
                                        <tr>
                                            <th >Employee Name</th>
                                            <th >QID Number</th>
                                            <th >QID Expiry Date</th>
                                            <th >Employee Company</th>
                                    </tr>"""
                    for qid_employee in qid_expire_soon:
                        body += """<tr>  
                                    <td>{}</td>
                                    <td>{}</td>
                                    <td >{}</td>
                                    <td >{}</td>
                                    </tr>
                                """.format(qid_employee.name, qid_employee.qid if qid_employee.qid else "",
                                            qid_employee.qid_expiry_date,qid_employee.company_id.name)
                        qid_employee.qid_last_notification_date = fields.Date.today()

                    body += """</table> <br/> <br/> <br/>"""

                if driving_license_expire_soon:
                    body += """
                    <p>Driving License will expire soon</p>
                    <table class="tb1">
                                        <tr>
                                            <th >Employee Name</th>
                                            <th >Driving License Number</th>
                                            <th >Driving License Expiry Date</th>
                                            <th >Employee Company</th>
                                    </tr>"""

                    for driving_license_employee in driving_license_expire_soon:
                        body += """<tr>  
                                    <td>{}</td>
                                    <td>{}</td>
                                    <td>{}</td>
                                    <td>{}</td>
                                    </tr>
                                """.format(driving_license_employee.name,
                                            driving_license_employee.driving_license_number if driving_license_employee.driving_license_number else "", \
                                            driving_license_employee.driving_license_expiry_date,driving_license_employee.company_id.name)
                        driving_license_employee.driving_license_last_notification_date = fields.Date.today()
                    body += """</table> <br/> <br/> <br/>"""

                if health_care_card_expire_soon:
                    body += """
                    <p>Health Care Card will expire soon</p>
                    <table class="tb1">
                                        <tr>
                                            <th >Employee Name</th>
                                            <th >Health Care Card Number</th>
                                            <th >Health Care Card Expiry Date</th>
                                            <th >Employee Company</th>
                                    </tr>"""

                    for health_care_card in health_care_card_expire_soon:
                        body += """<tr>  
                                    <td>{}</td>
                                    <td>{}</td>
                                    <td>{}</td>
                                    <td>{}</td>
                                    </tr>
                                """.format(health_care_card.name, health_care_card.health_care_card_no,
                                            health_care_card.health_care_card_expiry_date,health_care_card.company_id.name)
                        health_care_card.health_care_card_last_notification_date = fields.Date.today()
                    body += """</table> <br/> <br/> <br/>"""

                email_values = {
                    'subject': "Employees' Document Will expire soon",
                    'body_html': body,
                    'email_layout_xmlid': 'mail.mail_notification_light',
                    'parent_id': False,
                    'attachment_ids': [],
                    'auto_delete': False,
                    'email_from': res.email,
                }
                partners = res.partner_ids
                for part in partners:
                    if part.email:
                        email_values["email_to"] = part.email
                        self.env['mail.mail'].sudo().create(email_values).send()
