# -*- coding: utf-8 -*-
################################################################################
#
#    AAHB-Service Ltd. (https://www.3bdalla3adil.github.io)
#    Author: ABDULLA BASHIR
#
################################################################################
from odoo import fields, models, api

# ACCOUNT PAYMENT
class AccountPayment(models.Model):
    """A class that inherits the already existing model account payment to add
    the related property contract and payment records"""
    _inherit = 'account.payment'

    unit_id = fields.Many2one('property.unit', related='move_id.unit_id', string='Related Unit', store=True) #compute='_compute_unit_id'
    cheque_no = fields.Char(string='Cheque No', related='move_id.cheque_no', store=True)
    pdc_state = fields.Selection([('deposited', 'Deposited'), ('rejected', 'Rejected'),
                                  ('returned', 'Returned'),('cleared', 'Cleared')], string='Cheque Status')

# ACCOUNT INVOICE
class AccountMove(models.Model):
    """A class that inherits the already existing model account move to add
    the related property contract and payment records"""
    _inherit = 'account.move'

    pdc_name = fields.Char(string='Cheque Number', required=False, tracking=True)
    pdc_state = fields.Selection(
        [('deposited', 'Deposited'), ('rejected', 'Rejected'), ('returned', 'Returned'),
         ('cleared', 'Cleared')], string='Cheque Status')
    payment_mode = fields.Selection([('cheque', 'Cheque'), ('cash', 'Cash'), ('transfer', 'Transfer')],
                                    string='Payment Mode', default='cheque')
    cheque_date = fields.Date(string='Cheque Date', )
    cheque_no = fields.Char(string='Cheque No', )
    monthly_rent = fields.Float(string='Current Rent', )
    partner_id = fields.Many2one('res.partner', string='Contract', )
    unit_id = fields.Many2one('property.unit',related='partner_id.unit_id', string='Related Unit', store=True) #compute='_compute_unit_id'
    mobile = fields.Char(string='Mobile No', compute='_compute_mobile_no', store= True)
    customer_id = fields.Char(string='Customer ID', compute='_compute_customer_id',)

    account_id = fields.Many2one('account.account', string='Account', )

    rent_deposit_account = fields.Many2one('res.bank', string='Deposit Bank')

    deposit_amount = fields.Char('Deposit Amount')
    deposit_type = fields.Selection([('bank', 'Bank'), ('cash', 'Cash')], string='Deposit Type')
    deposit_date = fields.Date('Deposit Check Date')

    def action_deposit(self):
        return self.write({'pdc_state': 'deposit'})
        # for rec in self:
        #     rec.pdc_state = 'deposited'

    def action_revert(self):
        return self.write({'pdc_state': 'draft'})
        # for rec in self:
        #     rec.pdc_state = 'draft'

    def action_reject(self):
        return self.write({'pdc_state': 'rejected'})
        # for rec in self:
        #     rec.pdc_state = 'rejected'

    def action_return(self):
        return self.write({'pdc_state': 'returned'})
        # for rec in self:
        #     rec.pdc_state = 'returned'

    # def done(self):

    def action_clear(self):
        return self.write({'pdc_state': 'cleared'})
        # for rec in self:
        #     rec.pdc_state = 'cleared'

    @api.model
    def _get_view(self, view_id=None, view_type='tree', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        active_company = self.env.company
        #TO FIX LAGGING ISSUE IN PRODUCTION
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
        #         node.set('invisible', '1')
        if view_type == 'form':
            for node in arch.xpath("//field[@name='name']"):
                node.set('string', 'Invoice Number')
        return arch, view

    # @api.depends('partner_id')
    # def _compute_unit_id(self):
    #     self.unit_id = self.partner_id.unit_id.id

    @api.depends('partner_id')
    def _compute_mobile_no(self):
        for rec in self:
            rec.mobile = rec.partner_id.mobile

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            rec.unit_id = rec.partner_id.unit_id.id
        # self.customer_id = self.partner_id.id
        # self.mobile = self.partner_id.mobile

    @api.depends('partner_id')
    def _compute_customer_id(self):
        self.customer_id = str(self.partner_id.id)

    @api.model
    def create(self, vals):
        for record in self:
            if 'company_id' not in vals:
                vals['company_id'] = self.env.user.company_id.id

            # Check if the company_id is 1
            if vals['company_id'] == 1:
                if vals.get('name', 'New') == 'New':
                    from datetime import datetime
                    seq_date = datetime.now().strftime('%Y')
                    seq = self.env['ir.sequence'].next_by_code('account.move') or '/'
                    vals['name'] = f"{vals['unit']}/{seq_date}/{seq}"
                    vals['cheque_no'] = f"{vals['unit']}/{record.unit_id.generate_sequence()}"

        return super(AccountMove, self).create(vals)
    # payment_number 2024/125,2024/126,
