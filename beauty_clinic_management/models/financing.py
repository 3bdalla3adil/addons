# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
#from mock import DEFAULT
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class FinancingAgreement(models.Model):
    _name = 'financing.agreement'
    _description = "Financing Aggreement"
    
    type_of_service =  fields.Char('Type of Service')
    date_of_service =  fields.Date('Date of Service')
    total_amount_to_be_financed =  fields.Float('Total amount to be financed')
    date_to_be_paid =  fields.Date('Date to be paid')
    payment_id =  fields.One2many ('payment.schedule','financing_id',"Payment Schedule")
    payment_by_cash_check =  fields.Float('Payment made by cash or check')
    payment_by_credit_card =  fields.Float('Payment made by credit card ')
    credit_card_type =  fields.Selection([('visa', 'Visa'), ('mastercard', 'MasterCard'), ('other', 'Other')], string='Credit Card Type',default='visa' )
    name_as_appears_on_card =  fields.Char('Name as appears on card')
    name = fields.Many2one('medical.patient', 'Name of Patient')
    expiry_month =  fields.Char('Expiry Month')
    expiry_year =  fields.Char('Expiry Year')
    is_credit_card =  fields.Boolean('Credit Card')
    credit_card_number =  fields.Char('Credit Card Number')
    invoice_id1 = fields.Many2one('account.move', 'Invoice Number')

    @api.model
    def default_get(self, fields):
        res = super(FinancingAgreement, self).default_get(fields)
        invoice_obj = self.env['account.move'].browse(self._context.get('active_ids'))
        if invoice_obj:
            medical_search = self.env['medical.patient'].search([('name', '=', invoice_obj.partner_id.id)])
            res['name'] = medical_search.id
            res['total_amount_to_be_financed'] = invoice_obj.residual
            res['date_of_service'] = invoice_obj.date_invoice
            res['type_of_service'] = ''
            for inv in invoice_obj.invoice_line_ids:
                res['type_of_service'] += inv.product_id.name + ','
            res['invoice_id1'] = invoice_obj.id
            return res
        else:
            return res

    @api.model
    def create(self, vals):
        res = super(FinancingAgreement, self).create(vals)
        active_ids = self._context.get('active_ids')
        if active_ids:
            inv_brw = self.env['account.move'].browse(active_ids)
            ret = inv_brw.write({'finance_id': res.id})
        return res
    
    
#     def create(self, cr, uid, vals, context):
#         
#         from openerp import fields
#         current_year = datetime.datetime.strptime(fields.Datetime.now(), DEFAULT_SERVER_DATETIME_FORMAT).strftime("%Y")
#          
#         if vals.has_key('expiry_year') and vals['expiry_year']!= False and int(vals['expiry_year']) < int(current_year) :
#             raise osv.except_osv(_("Warning"),_("Credit Card Expiry year should be greater than %d") % (int(current_year)-1))
#           
#         
#         if vals.has_key('expiry_month') and vals['expiry_month']!= False and (int(vals['expiry_month']) >12 or  int(vals['expiry_month']) <1) :
#             raise osv.except_osv(_("Warning"),_("Credit Card Expiry month should be in between 1 to 12") )
#         
#         return super(financing_agreement, self).create(cr, uid, vals, context)
#      
#      
#      
#     def write(self, cr, uid, ids, vals, context):
#         from openerp import fields
#         for id in ids :
#             financing_agreement_rec = self.browse(cr, uid, id, context)
#             current_year = datetime.datetime.strptime(fields.Datetime.now(), DEFAULT_SERVER_DATETIME_FORMAT).strftime("%Y")
#              
#             if vals.has_key('expiry_year') and vals['expiry_year'] :
#                 expiry_year = vals['expiry_year']
#             else :
#                 expiry_year = financing_agreement_rec.expiry_year
#                  
#             if int(expiry_year) < int(current_year) and expiry_year != False:
#                 raise osv.except_osv(_("Warning"),_("Credit Card Expiry year should be greater than %d") % (int(current_year)-1))
#              
#              
#             if vals.has_key('expiry_month') and vals['expiry_month'] :
#                 expiry_month = vals['expiry_month']
#             else :
#                 expiry_month = financing_agreement_rec.expiry_month
#                 
#             if expiry_month != False and (int(expiry_month) < 1 or int(expiry_month) > 12) :
#                 raise osv.except_osv(_("Warning"),_("Credit Card Expiry month should be in between 1 to 12") )
#              
#             
#         return super(financing_agreement, self).write(cr, uid, ids, vals, context)


class PaymentSchedule(models.Model):
    _name = 'payment.schedule'
    _description = "Payment Schedule"
    
    name =  fields.Char('Name')
    date =  fields.Date('Date')
    amount_to_be_paid =  fields.Float('Amount to be paid')
    financing_id =  fields.Many2one('financing.agreement','Financing Agreement')

