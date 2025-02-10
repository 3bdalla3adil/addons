# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
#from mock import DEFAULT
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = ("Sale Order")

    @api.depends('patient_id')
    def _compute_patient(self):
        patient_obj = self.env['medical.patient']
        for rec in self:
            patient_id = patient_obj.search([('partner_id', '=', rec.partner_id.id)]).id
            rec.patient_id = patient_id

    patient_id = fields.Many2one('medical.patient', compute="_compute_patient", string="Patient")
    doctor = fields.Many2one('medical.doctor', 'Doctor')
    clinic = fields.Many2one('medical.clinic', 'Clinic')
    insurance_company = fields.Many2one('res.partner', 'Insurance Company',
                                        domain=[('is_insurance_company', '=', True)])
    appointment_id = fields.Many2one('medical.appointment', 'Appointment')



    def _prepare_invoice(self):
        invoice_vals = {
            'ref': self.client_order_ref or '',
            'move_type': 'out_invoice',
            # 'narration': self.comments,
            'invoice_user_id': self.user_id and self.user_id.id,
            'invoice_origin': self.name,
            'payment_reference': self.reference,
            #'transaction_ids': [Command.set(self.transaction_ids.ids)],
    #       #'company_id': self.company_id.id,
            'partner_id': self.patient_id.partner_id.id,
            'patient': self.patient_id.id,
            'invoice_line_ids': [],
            'clinic': self.clinic.id,
            'doctor': self.doctor.id,  # APPROVED
            'invoice_date': datetime.today()
        }
        return invoice_vals


    def create_invoices(self):
        # if not self.prescription_line:
        #     raise UserError(_("Please add medicine line."))
        invoice_vals = self._prepare_invoice()
        # for line in self.prescription_line:
        #     res = {}
        #     res.update({
        #         # 'name': line.medicine_id.name.name,
        #         'product_id': line.medicine_id.name.id,
        #         'price_unit': line.medicine_id.price,
        #         'quantity': line.quantity,
        #     })
        #     invoice_vals['invoice_line_ids'].append((0, 0, res))
        inv_id = self.env['account.move'].create(invoice_vals)
        #res = super(SaleOrder, self).create_invoice()
        return inv_id



# DONE!
class AccountInvoice(models.Model):
    _inherit = "account.move"
    _description = "Account Invoice"
    
    finance_id = fields.Many2one('financing.agreement', 'Financing Agreement')
    doctor = fields.Many2one('medical.doctor', 'Doctor')
    clinic = fields.Many2one('medical.clinic', 'Clinic')
    insurance_company = fields.Many2one('res.partner', 'Insurance Company',
                                        domain=[('is_insurance_company', '=', True)])
    patient_id = fields.Many2one('res.partner', 'Patient')
    appointment_id = fields.Many2one('medical.appointment', 'Appointment')

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        active_company = self.env.company
        # if view_type == 'form' and active_company.id == 1:
        #     for node in arch.xpath("//field[@name='clinic']"):
        #         node.set('invisible', '1')
        #     for node in arch.xpath("//field[@name='doctor']"):
        #         node.set('invisible', '1')
        #     for node in arch.xpath("//field[@name='insurance_company']"):
        #         node.set('invisible', '1')
        #     for node in arch.xpath("//field[@name='patient_id']"):
        #         node.set('invisible', '1')
        #     for node in arch.xpath("//field[@name='appointment_id']"):
        #         node.set('invisible', '1')
        #     for node in arch.xpath("//field[@name='finance_id']"):
        #         node.set('invisible','1')
#TO FIX LAGGING
        # if view_type == 'form' and active_company.id != 1:
        #
        #     for node in arch.xpath("//field[@name='cheque_no']"):
        #         node.set('invisible','1')
        #     for node in arch.xpath("//field[@name='mobile']"):
        #         node.set('invisible','1')
        #     for node in arch.xpath("//field[@name='customer_id']"):
        #         node.set('invisible','1')
        #     for node in arch.xpath("//field[@name='pdc_state']"):
        #         node.set('invisible','1')

        for node in arch.xpath("//field[@name='name']"):
            node.set('string', 'Invoice Number')
        return arch, view

    def financial_agreement_action_inherit1(self):
        finance_id = self.finance_id
        if finance_id:
            return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'financing.agreement',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_id': finance_id.id,
                    'views': [(False, 'form')],
                    }
        else:
            return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'financing.agreement',
                    'view_mode': 'form',
                    'view_type': 'form',
                    'views': [(False, 'form')],
                    }

#
# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
#
#     group_display_incoterm = fields.Boolean('Group Display Incoterm')