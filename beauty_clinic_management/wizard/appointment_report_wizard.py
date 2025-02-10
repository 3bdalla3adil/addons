from odoo import models, fields, api

from odoo.exceptions import UserError


#ToDo: Make Appointment Daily Report generated from Wizard - DONE!

class AppointmentReportWizard(models.TransientModel):
    _name = 'appointment.report.wizard'
    _description = 'appointment Report Wizard'

    start_date = fields.Datetime(string="Start Date", required=True)
    end_date = fields.Datetime(string="End Date", required=True)

    def generate_report(self):
        datas = {
            'active_ids': self.env.context.get('active_ids', []),
            'form':self.read(['end_date', 'start_date'])[0],
                }

        res = self.env.ref('beauty_clinic_management.action_report_appointments').report_action(self, data=datas)
        return res
