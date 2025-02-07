# -*- coding: utf-8 -*-
################################################################################
#
#    AAHB-Service Ltd. (https://www.3bdalla3adil.github.io)
#    Author: ABDULLA BASHIR
#
################################################################################
from odoo import models, fields, api



class AccountPDC(models.Model):
    _name = 'account.pdc'
    _description = 'Post Dated Cheque'

    name = fields.Char(string='Cheque Number',required=False,)



# class PDCPayment(models.Model):
#     _name = 'pdc.payment'
#     _description = 'Post Dated Cheque Payment'
#
#     pdc_id = fields.Many2one('account.pdc',string='')
#     payment_mode = fields.Selection([('cheque', 'Cheque'), ('cash', 'Cash'), ('transfer', 'Transfer')],
#                                     string='Payment Mode')
#     cheque_date = fields.Date(string='Cheque Date', required=True)
#
#     paid_amount = fields.Float(string='Paid Amount',default='pdc_id.')
