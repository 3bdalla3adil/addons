# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date


class HRDependats(models.Model):
    _name = 'hr.dependants'
    _description = 'HR Dependants'

    name = fields.Char('Name', required=True)
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')], string='Gender', required=True)
    dob = fields.Date('Date of Birth', required=True)
    age = fields.Integer('Age', compute='_compute_age')
    sponsor = fields.Selection([('employee', 'Employee'),
                                ('Others', 'Others')], 'Sponsor')
    employee_id = fields.Many2one('hr.employee', 'Employee', ondelete='cascade')

    @api.depends('dob')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.dob:
                year_difference = today.year - rec.dob.year - ((today.month, today.day) < (rec.dob.month, rec.dob.day))
                rec.age = year_difference
            else:
                rec.age = 0
