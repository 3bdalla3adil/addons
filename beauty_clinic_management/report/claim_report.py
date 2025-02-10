from odoo import api, models, _
from odoo.exceptions import UserError


class ClaimReport(models.AbstractModel):
    _name='report.beauty_clinic_management.claim_report'
    _description = "Dental Management Report Claim"
    
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
#         final_records = self.env['dental.insurance.claim.management'].search \
#             ([('claim_date', '>=', from_date), ('claim_date', '<=', to_date)])
        inv_records = self.env['account.move'].search([
            ('invoice_date', '>=', from_date),('invoice_date', '<=', to_date),('patient','!=',False)
        ])
        return {
            'doc_ids': self.ids,
            'doc_model': 'dental.claim.wizard',
            'data': data['form'],
            'docs': docs,
            'patients': inv_records,
        }
        
class AppointmentReport(models.AbstractModel):
    _name = 'report.beauty_clinic_management.report_appointments_template'
    _description = 'Appointment Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']

        # claims = self.env['claim.request'].browse([
        appointments = self.env['medical.appointment'].search([ # use search() instead of browse()
            ('appointment_sdate', '>=', start_date),
            ('appointment_sdate', '<=', end_date),
        ])
        from datetime import datetime
        start_date = datetime.strptime(data['form'].get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(data['form'].get('end_date'), '%Y-%m-%d')
        return {
            'doc_ids': self.ids,
            'doc_model': 'medical.appointment',
            'data': data['form'],
            'docs': docs,
            'appointments': appointments,
            'start_date': start_date.strftime('%d-%m-%Y'),
            'end_date': end_date.strftime('%d-%m-%Y'),
            # 'group': group,
        }

