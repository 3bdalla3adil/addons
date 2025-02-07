from odoo import models, api

class ClaimRequestReport(models.AbstractModel):
    _name = 'claim.request.report'
    _description = 'Claim Request Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data:
            docs = self.env['claim.request'].browse(data['claim_requests'])
        else:
            docs = self.env['claim.request'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'claim.request',
            'docs': docs,
        }
