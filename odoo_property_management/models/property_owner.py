# -*- coding: utf-8 -*-
from odoo import models, fields, api

  #===========================================================================================================
  #==== PIPELINE ============ Owner Details ==> ... ================================================
  #===========================================================================================================

  #ToDo:


class PropertyOwner(models.Model):
    _name = 'property.owner'
    # _inherit = 'res.partner'
    _description = 'Owner Details'

    code = fields.Many2one('property.property','Related Property Code')
    ar_name = fields.Char('Arabic Name')
    en_name = fields.Char('English Name')
    email = fields.Char('Owner Email')
    sms = fields.Char('Owner Sms Number')

    payment_serial_no = fields.Char('Owner Payment Serial No')
    deposit_serial_no = fields.Char('Owner Deposit Serial No')
    adjustment_serial_no = fields.Char('Owner Adjustment Serial No')
    # company_id = fields.Many2one('res.company')


