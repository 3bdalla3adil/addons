from datetime import datetime

from odoo import models, api, _

from odoo.exceptions import UserError

from isodate import strftime


class ClaimRequestReport(models.AbstractModel):
    _name = 'report.odoo_property_management.report_claims_template'
    _description = 'Claim Request Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form') or not self.env.context.get('active_model') or not self.env.context.get('active_id'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        start_date = data['form']['start_date']
        end_date = data['form']['end_date']
        group = data['form']['group'] # Gives key error
        state = data['form']['state'] # Added for Bassam

        user = self.env.user.name
        # claims = self.env['claim.request'].browse([
        # Define your search domain
        domain = [
            ('claim_date', '>=', start_date),
            ('claim_date', '<=', end_date),
            ('group', '=', group)
        ]

        # Add the state filter only if state is not False
        if state:
            domain.append(('state', '=', state))
        if user == 'ISMAIL':
            domain.append(('state', '!=', 'done'))

        # Perform the search with the updated domain
        claims = self.env['claim.request'].search(domain)

        # claims = self.env['claim.request'].search([ # use search() instead of browse()
        #     ('claim_date', '>=', start_date),
        #     ('claim_date', '<=', end_date),
        #     ('group', '=', group),
        #     ('state', '=', state),
        # ])
        start_date = datetime.strptime(data['form'].get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(data['form'].get('end_date'), '%Y-%m-%d')
        return {
            'doc_ids': self.ids,
            'doc_model': 'dental.claim.wizard',
            'data': data['form'],
            'docs': docs,
            'claims': claims,
            'start_date': start_date.strftime('%d-%m-%Y'),
            'end_date': end_date.strftime('%d-%m-%Y'),
            'user': user,
            # 'group': group,
        }
