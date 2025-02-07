# -*- coding: utf-8 -*-
################################################################################
#
#    AAHB-Service Ltd. (https://www.3bdalla3adil.github.io)
#    Author: ABDULLA BASHIR
#
################################################################################
from odoo import models, fields, api


#===========================================================================================================
#==== PIPELINE ============ SponsorShip Type  ==> ... ============================
#===========================================================================================================

#ToDo: SponsorShip - Done!

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    sponsorship = fields.Selection([('Family','0'),
                                    ('Company','1'),
                                    ('Outside','2')],string='Sponsorship Type',)
