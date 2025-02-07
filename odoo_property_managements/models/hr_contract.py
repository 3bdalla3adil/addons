# -*- coding: utf-8 -*-
################################################################################
#
#    AAHB-Service Ltd. (https://www.3bdalla3adil.github.io)
#    Author: ABDULLA BASHIR
#
################################################################################

from odoo import models, fields, api


#===========================================================================================================
#==== PIPELINE ============  ==> ... ============================
#===========================================================================================================

#ToDo:


class HrContract(models.Model):
    _inherit = 'hr.contract'

    emp_id = fields.Char(compute='_compute_emp_id',string='EID No',store=True)


    def _compute_emp_id(self):
        self.emp_id = str(self.employee_id.id)