from odoo import models, fields, api

from odoo.exceptions import UserError


#ToDo: Make Claim Weekly Report generated from Wizard

class ClaimReportWizard(models.TransientModel):
    _name = 'claim.report.wizard'
    _description = 'Claim Report Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    group = fields.Selection([('a', 'A'), ('b', 'B')], string="Group", required=True)

    def generate_report(self):

        claim_obj = self.env['claim.request']
        for rec in self:
            domain = [
                ('claim_date', '>=', rec.start_date),
                ('claim_date', '<=', rec.end_date),
                ('group', '=', rec.group)
            ]
            claims = claim_obj.search(domain)
            if not claims:
                raise UserError("No claims found for the given criteria.")

            data = {
                'model': 'claim.request',
                'docs': claims,
            }
            res = self.env.ref('odoo_property_management.action_report_claims').report_action(self, data=data)
        return res
