from odoo import models, fields, api, _

class MedicalProcedure(models.Model):
    _description = "Medical Procedure"
    _name = "medical.procedure"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(['|', ('name', operator, name), ('description', operator, name)])
        if not recs:
            recs = self.search([('name', operator, name)])
        return recs.name_get()

    # SET APPOINTMENT Based On Patient
    # @api.depends('patient_id')
    # def _compute_appt_id(self):
    #     if self.patient_id:
    #         self.appt_id = self.patient_id.apt_id

    name = fields.Char('Code', size=128, required=True)
    description = fields.Char('Long Text', size=256)
