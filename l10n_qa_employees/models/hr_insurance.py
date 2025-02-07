# -*- coding: utf-8 -*-

from odoo import models, fields


class HRInsurance(models.Model):
    _name = 'hr.insurance.qa'
    _description = 'HR Insurance'

    name = fields.Char('Membership No', required=True)
    cls = fields.Char('Class', required=True)
    insurer_id = fields.Many2one('res.partner', 'Insurance Provider', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    state = fields.Many2one('insurance.state', 'Status')
    employee_id = fields.Many2one('hr.employee', 'Employee', ondelete='cascade')


class InsuranceState(models.Model):
    _name = 'insurance.state'
    _description = 'Insurance State'

    name = fields.Char('Name')
