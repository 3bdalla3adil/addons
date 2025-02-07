# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    partner_ids = fields.Many2many("res.partner", string='Documents Responsible(s)', related='company_id.partner_ids', readonly=False)


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    partner_ids = fields.Many2many("res.partner", string='Documents Responsible(s)')