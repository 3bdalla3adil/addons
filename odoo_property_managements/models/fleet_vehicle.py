# -*- coding: utf-8 -*-
################################################################################
#
#    AAHB-Service Ltd. (https://www.3bdalla3adil.github.io)
#    Author: ABDULLA BASHIR
#
################################################################################
from odoo import models, fields, api, _


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    _description = 'Vehicle'

    #chasis_no = fields.Char('Chasis No')
    # engin_no = fields.Char('Engine No')
    engin_no = fields.Char('Engine No')
    insurance_company = fields.Char('Insurance Company')
    insurance_policy = fields.Char('Insurance Policy')
    insurance_coverage = fields.Char('Insurance Coverage')
    insurance_amount = fields.Float('Insurance Amount')
    insurance_expiry = fields.Date('Insurance Expiry')
    istimara_expiry = fields.Date('Istimara Expiry')
    insurance_type = fields.Selection([('full','Full'),('against_others','Against Others'),])

    # FROM THE GPT :
    def _check_vehicle_documents(self):
        """
        Check each vehicle for expired or soon-to-expire insurance or istimara documents.
        Create a mail.activity reminder for the vehicle's manager if needed.
        """
        # Define the threshold: e.g., reminder 15 days before expiry
        from datetime import timedelta
        reminder_threshold = fields.Date.today() + timedelta(days=15)
        today = fields.Date.today()

        for vehicle in self.search([]):
            messages = []
            manager = vehicle.manager_id

            # Check Insurance Expiry
            if vehicle.insurance_expiry:
                if vehicle.insurance_expiry <= today or vehicle.insurance_expiry <= reminder_threshold:
                    messages.append(_("Insurance expired on %s") % vehicle.insurance_expiry)

            # Check Istimara Expiry
            if vehicle.istimara_expiry:
                if vehicle.istimara_expiry <= today or vehicle.istimara_expiry <= reminder_threshold:
                    messages.append(_("Istimara expired on %s") % vehicle.istimara_expiry)

            # If any document needs update and there's a manager assigned, create an activity
            if messages and manager:
                reminder_message = ", ".join(messages)
                activity_vals = {
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _("Update Vehicle Documents: ") + reminder_message,
                    'date_deadline': today,
                    'user_id': manager.id,
                    'res_model_id': self.env['ir.model']._get('fleet.vehicle').id,
                    'res_id': vehicle.id,
                }
                self.env['mail.activity'].create(activity_vals)

                # Optionally, send an instant bus notification
                bus_message = {
                    "type": "info",
                    "message": _("Vehicle %s requires document update: %s") % (vehicle.name, reminder_message),
                    "title": _("Vehicle Document Reminder"),
                    "sticky": False,
                }
                notifications = [[manager.partner_id.id, "web.notify", [bus_message]]]
                self.env["bus.bus"]._sendmany(notifications)

        return True
    # ==============
    def send_documents_expiry_email(self):
        from datetime import timedelta

        # lagally_to_renotify = fields.Date.today() + timedelta(days=14)
        soon_expiry_date = fields.Date.today() + timedelta(days=30)
        company = self.env['res.company'].sudo().search([])
        for res in company:
            # changed health card to Insurance_expiry:
            qid_expire_soon = self.sudo().search(['&', ("insurance_expiry", "<=", soon_expiry_date),
                                        ('company_id', '=', res.id)])

            driving_license_expire_soon = self.sudo().search(['&', ("istimara_expiry", "<=", soon_expiry_date),
                                                ('company_id', '=', res.id)])
            # changed health card to Istimara_expiry:
            # health_care_card_expire_soon = self.sudo().search(['&', ("istimara_expiry", "<=", soon_expiry_date), '|',
            #                                     ("health_care_card_last_notification_date", ">",lagally_to_renotify),
            #                                     ("health_care_card_last_notification_date", "=", False),
            #                                     ('company_id', '=', res.id)])
            # passport_expire_soon = self.sudo().search(['&', ("passport_expiry_date", "<=", soon_expiry_date), '|',
            #                             ("passport_last_notification_date", ">", lagally_to_renotify),
            #                             ("passport_last_notification_date", "=", False),
            #                             ('company_id', '=', res.id)])
            if qid_expire_soon or driving_license_expire_soon :
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


                if qid_expire_soon:
                    body += """
                    <p>QID will expire soon</p>
                    <table class="tb1 table table-sm o_main_table">
                                        <tr>
                                            <th >Employee Name</th>
                                            <th >engin_no Number</th>
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
                                """.format(qid_employee.licence_plate, qid_employee.engin_no if qid_employee.engin_no else "",
                                            qid_employee.insurance_expiry,qid_employee.company_id.name)
                        qid_employee.qid_last_notification_date = fields.Date.today()

                    body += """</table> <br/> <br/> <br/>"""

                if driving_license_expire_soon:
                    body += """
                    <p>Driving License will expire soon</p>
                    <table class="tb1">
                                        <tr>
                                            <th >Licence Plate</th>
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
                                            driving_license_employee.engine_no if driving_license_employee.engine_no else "", \
                                            driving_license_employee.istimara_expiry,driving_license_employee.company_id.name)
                        driving_license_employee.driving_license_last_notification_date = fields.Date.today()
                    body += """</table> <br/> <br/> <br/>"""

                # if health_care_card_expire_soon:
                #     body += """
                #     <p>Health Care Card will expire soon</p>
                #     <table class="tb1">
                #                         <tr>
                #                             <th >Employee Name</th>
                #                             <th >Health Care Card Number</th>
                #                             <th >Health Care Card Expiry Date</th>
                #                             <th >Employee Company</th>
                #                     </tr>"""
                #
                #     for health_care_card in health_care_card_expire_soon:
                #         body += """<tr>
                #                     <td>{}</td>
                #                     <td>{}</td>
                #                     <td>{}</td>
                #                     <td>{}</td>
                #                     </tr>
                #                 """.format(health_care_card.name, health_care_card.health_care_card_no,
                #                             health_care_card.istimara_expiry,health_care_card.company_id.name)
                #         health_care_card.health_care_card_last_notification_date = fields.Date.today()
                #     body += """</table> <br/> <br/> <br/>"""

                email_values = {
                    'subject': "Vehicle' Document Will expire soon",
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
