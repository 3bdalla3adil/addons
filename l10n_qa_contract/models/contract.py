# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class Contract(models.Model):
    _inherit = "hr.contract"

    date_start = fields.Date(string="Joining Date",
                             help="The actual joining date, the benefits are computed based on this date.")
    contract_date = fields.Date("Contract Date", help="Contract signing date")
    authenticating_date = fields.Date("Authenticating Date",
                                      help="Fill the field with the official authenticating date")
    service_years = fields.Integer(compute='_get_service_years', default=0)
    # flags
    year_5_flag = fields.Boolean(default=False, copy=False)
    year_10_flag = fields.Boolean(default=False, copy=False)

    @api.depends("date_start")
    def _get_service_years(self):
        for contract in self:
            difference_in_years = int(relativedelta(fields.Date.today(), contract.date_start).years)
            contract.service_years = difference_in_years or 0

    def _cron_job_employee_service_years(self):
        contracts = self.search([('state', '=', 'open')])      
        body = """
                     <div style="width: 600px; margin-top: 5px;">
                        <div>Dear %s,</div>
                        <br/>
                        <p>
                            Please note that %s have been in %s for %s years.  
                        </p>
                        <br/>
                        <p>
                          Best Regards,
                        </p>
                    </div>
                """
        time_off_installed = self.env['ir.module.module'].search(
            [('name', '=', 'hr_holidays'), ('state', '=', 'installed')])
        administrator_ids = []
        activity_obj = self.env['mail.activity']
        activity_type_id = self.env.ref('mail.mail_activity_data_todo').id
        contract_model_id = self.env['ir.model']._get_id("hr.contract")
        for contract in contracts:
            employee_id = contract.employee_id
            users = self.env['res.users'].search(
                [('groups_id', '=', self.env.ref('hr_contract.group_hr_contract_manager').id),('company_ids','in',employee_id.company_id.id)])
            partner_ids = users.mapped('partner_id.id')
            if time_off_installed:
                time_off_administrators = self.env['res.users'].search(
                    [('groups_id', '=', self.env.ref('hr_holidays.group_hr_holidays_manager').id),('company_ids','in',employee_id.company_id.id)])
                administrator_ids = time_off_administrators.mapped('partner_id.id')
            if contract.service_years == 5 and not contract.year_5_flag:
                body_5 = body % ("Contract Administrator", employee_id.name, employee_id.company_id.name, "5")
                if users:
                    self.env['mail.mail'].sudo().create({
                                                    'recipient_ids': partner_ids,
                                                    'subject': '5 years notification',
                                                    'body_html': body_5}).send()
                body_5 = body % ("HR responsible", employee_id.name, employee_id.company_id.name, "5")
                if contract.hr_responsible_id and contract.hr_responsible_id not in users:
                    self.env['mail.mail'].sudo().create({
                                                    'email_to': contract.hr_responsible_id.partner_id.email,
                                                    'subject': '5 years notification',
                                                    'body_html': body_5}).send()
                body_5 = body % (employee_id.name, "you", employee_id.company_id.name, "5")
                self.env['mail.mail'].sudo().create({'email_to': employee_id.work_email,
                                                     'subject': '5 years notification',
                                                     'body_html': body_5}).send()
                if time_off_installed:
                    leave_manager_id = contract.employee_id.leave_manager_id
                    if time_off_administrators:
                        for admin in time_off_administrators:
                            activity_obj.create({
                                'res_id': contract.id,
                                'res_model_id': contract_model_id,
                                'activity_type_id': activity_type_id,
                                'user_id': admin.id,
                                'summary': '%s years re-allocation' % "5",
                                'date_deadline': fields.Date.today(self)})
                    if leave_manager_id and leave_manager_id not in time_off_administrators:
                        activity_obj.create({
                            'res_id': contract.id,
                            'res_model_id': contract_model_id,
                            'activity_type_id': activity_type_id,
                            'user_id': leave_manager_id.id,
                            'summary': '%s years re-allocation' % "5",
                            'date_deadline': fields.Date.today(self)})
                contract.year_5_flag = True

            elif contract.service_years == 10 and not contract.year_10_flag:
                body_10 = body % ("Contract Administrator", employee_id.name, employee_id.company_id.name, "10")
                if users:
                    self.env['mail.mail'].sudo().create({
                                                    'recipient_ids': partner_ids,
                                                    'subject': '10 years notification',
                                                    'body_html': body_10}).send()
                body_10 = body % ("HR responsible", employee_id.name, employee_id.company_id.name, "10")
                if contract.hr_responsible_id and contract.hr_responsible_id not in users:
                    self.env['mail.mail'].sudo().create({
                                                    'email_to': contract.hr_responsible_id.partner_id.email,
                                                    'subject': '10 years notification',
                                                    'body_html': body_10}).send()
                body_10 = body % (employee_id.name, "you", employee_id.company_id.name, "10")
                self.env['mail.mail'].sudo().create({'email_to': employee_id.work_email,
                                                     'subject': '10 years notification',
                                                     'body_html': body_10}).send()
                if time_off_installed:
                    leave_manager_id = contract.employee_id.leave_manager_id
                    if time_off_administrators:
                        for admin in time_off_administrators:
                            activity_obj.create({
                                'res_id': contract.id,
                                'res_model_id': contract_model_id,
                                'activity_type_id': activity_type_id,
                                'user_id': admin.id,
                                'summary': '%s years re-allocation' % "10",
                                'date_deadline': fields.Date.today(self)})
                    if leave_manager_id and leave_manager_id not in time_off_administrators:
                        activity_obj.create({
                            'res_id': contract.id,
                            'res_model_id': contract_model_id,
                            'activity_type_id': activity_type_id,
                            'user_id': leave_manager_id.id,
                            'summary': '%s years re-allocation' % "10",
                            'date_deadline': fields.Date.today(self)})

                contract.year_10_flag = True