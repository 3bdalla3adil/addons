# -*- coding: utf-8 -*-
################################################################################
#
#    AAHB-Service Ltd. (https://www.3bdalla3adil.github.io)
#    Author: ABDULLA BASHIR
#
################################################################################

from odoo import models, fields, api

from dateutil.relativedelta import relativedelta
from datetime import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner' # Contracts
    # _rec_name_search = models.Model._rec_names_search.append(['Unit_id','monthly_rent'])

    # view_priority = fields.Integer(string='View Priority', default=20)

    #contract remaining days

    date_since = fields.Date('Tenant Since')
    cheque_date = fields.Date('Cheque Date')
    # active = fields.Boolean(default=True)

    unit_id    = fields.Many2one('property.unit', 'Related Units')
    unit       = fields.Char(related='unit_id.display_name', string='Related unit')

    date_start = fields.Date('Start Date', required=True, default=fields.Date.today(), tracking=True, index=True)
    date_end   = fields.Date('End Date', tracking=True,
                           help="End date of the contract (if it's a fixed-term contract).")
    contract_name = fields.Char('Contractor Name')
    display_name = fields.Char(string='Contractor Name',compute='_compute_display_name')
    # bank_code = fields.Char(string='Customer Bank Code',)

    monthly_rent = fields.Float(string='Monthly Rent')

    invoice_ids = fields.One2many('account.move','partner_id', string='PDC Invoices')

    # rent_deposit_bank = fields.Char('Deposit Bank')
    rent_deposit_account = fields.Many2one('res.partner.bank', string='Deposit Bank Account')

    deposit_amount = fields.Char(string='Deposit Amount')
    deposit_type   = fields.Selection([('bank','Bank'),('cash','Cash')],string='Deposit Type')
    # payment_mode   = fields.Selection([('cheque','Cheque'),('cash','Cash'),('transfer','Transfer')],string='Payment Mode')
    deposit_date   = fields.Date(string='Deposit Check Date')

    account_id = fields.Many2one('account.account','Cheques Account')
    # deposit_bank = fields.Many2one('res.bank',string='Deposit Bank')
    # deposit_bank = fields.Many2one('res.bank','Deposit Bank')

    @api.onchange('unit_id')
    def onchange_unit_id(self):
        for rec in self:
            rec.monthly_rent = rec.unit_id.current_rent
            # rec.

    def action_generate_pdc(self):
        pdc_journal = self.env['account.journal'].search([('code','=','PDC')]).id
        # account = self.env['account.account'].search([('code', '=', '100107')], limit=1)
        # first_char = text.split('-')[0][0]


        for record in self:
            account = record.account_id

            previous_date = record.date_start
            current_date = record.cheque_date
            unit_seq_obj = self.env['property.unit.sequence']
            date_difference = record.cheque_date - record.date_start
            while current_date <= record.date_end:

                seq = self.env['ir.sequence'].next_by_code('account.pdc') or '/'
                seq = f"{record.unit}/{datetime.today().strftime('%Y/')}{seq}"
                vals = {
                    "name": seq,
                    "date": fields.Date.today(),
                    "ref": seq,
                    # "state": "draft",
                    "move_type": "out_invoice",
                    "user_id": self.env.user.id,
                    "invoice_date": current_date,
                    "invoice_date_due": current_date,
                    "partner_id": record.id,
                    "company_id": self.env.user.company_id.id,
                    "cheque_no": f'{record.unit}/{record.unit_id.generate_sequence()}',
                    # "journal_id": pdc_journal,
                    'invoice_line_ids': [(0, 0, {
                        'name': 'Rent for Property Unit %s For Month %s' % (record.unit, str(current_date.strftime("%B"))),
                        'quantity': 1,
                        'price_unit': record.monthly_rent,
                        'account_id':account.id
                    })],
                }
                invoices = self.env['account.move'].create(vals)
                # record.invoice_ids = (0, 0, vals)
                previous_date += relativedelta(months=1)
                current_date += relativedelta(months=1)
