from odoo import models, fields, api

from odoo.exceptions import UserError


#ToDo: Make Claim Weekly + Monthly Report generated from Wizard

class ClaimReportWizard(models.TransientModel):
    _name = 'claim.report.wizard'
    _description = 'Claim Report Wizard'

    start_date = fields.Date(string="Start Date", default=fields.Date.today, required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today, required=True)
    group = fields.Selection([('a', 'A'), ('b', 'B')], string="Group", default='b', required=False)
    state = fields.Selection([
        ('new', 'New'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'IN Progress'),
        ('done', 'Completed'),
    ], string="Claim Status", default='new', required=False)

    def generate_report(self):
        datas = {
            'active_ids': self.env.context.get('active_ids', []),
            'form':self.read(['end_date', 'start_date','group','state'])[0],
                }

        res = self.env.ref('odoo_property_management.action_report_claims').report_action(self, data=datas)
        return res
