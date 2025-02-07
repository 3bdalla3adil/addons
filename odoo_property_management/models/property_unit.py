# -*- coding: utf-8 -*-
from odoo import models, fields, api

from email.policy import default


  #===========================================================================================================
  #==== PIPELINE ============ Building Details ==> ... ================================================
  #========================== Unit Details     ==> ... ================================================
  #===========================================================================================================

  #ToDo:


# class UnitPartner(models.Model):
#     _inherit = 'res.partner'
#     _description = 'Unit Details'
#     _rec_name = 'display_name'
#     # blank = '000'
#
#     display_nam = fields.Char('Name', compute='_compute_display_nam',
#                                store=True)  # blank = '000' or building, compound => referenced property
#     number = fields.Char('Unit Number')  # blank = '000' or building, compound => referenced property
#     property_id = fields.Many2one(
#         comodel_name='res.partner', )  # blank = '000' or building, compound => referenced property
#     type_id = fields.Many2one(comodel_name='property.type', string='Unit Type')
#     unit_bld_code = fields.Char(related='property_id.bld_code', store=True,
#                            string='Related Property Code')  # compute='_compute_bld_code'
#     date_from = fields.Date(string='From')
#     date_to = fields.Date(string='Valid Till')
#     ra_no = fields.Char(string='RA NO')
#
#     claim_ids = fields.One2many('claim.request', 'claim_no', string='Claim Requests')
#     # asset_ids = fields.One2many('property.asset', 'asset_no', string='Assets')
#     is_furnitured = fields.Selection(
#         [('furnitured', 'Furnitured'), ('semi_furnitured', 'Semi Furnitured'), ('unfurnitured', 'Unfurnitured')])
#     is_electric = fields.Selection([('electricity_water', 'Electricity And Water'), ('no', 'No Electricity And Water')],
#                                    string='Electric&Water')
#     is_ac = fields.Selection([('ac', 'AC'), ('no', 'No AC')], string='AC')
#
#     # owner_id = fields.Many2one('property.owner', string='Owner Name')
#
#     bedroom = fields.Char(string='Bedrooms')
#     bathroom = fields.Char(string='Bathrooms')
#     water_no = fields.Char(string='Water No')
#     water_no1 = fields.Char(string='2nd Water No')
#     kahrma_no = fields.Char(string='kahrma No')
#     kahrma_no1 = fields.Char(string='2nd kahrma No')
#
#     idle_rent = fields.Float(string='Ideal Rent (QR)', default=0.0,
#                              digits='Product Price',
#                              help="Ideal Rent Price")  # Monetory
#
#     current_rent = fields.Float(string='Current Rent (QR)', default=0.0,
#                                 digits='Product Price',
#                                 help="Price at which the Property is Rented to Tenants.")  # Monetory
#     is_occupied = fields.Selection([('occupied', 'Occupied'), ('vacant', 'Vacant'), ('allocated', 'Allocated'), ],
#                                    string='Occupied/Vacant/Allocated')
#
#     contract_id = fields.Many2one('res.partner', string='Related Contracts')
#     # =================================
#     # =======Unit SEQUENCE=============
#     # =================================
#     sequence_ids = fields.One2many('property.unit.sequence', 'unit_id', string='Sequences')
#
#     @api.model
#     def create(self, vals):
#         record = super(UnitPartner, self).create(vals)
#         self.env['property.unit.sequence'].create({'unit_id': record.id})
#         return record
#
#     def generate_sequence(self):
#         for record in self:
#             seq = self.env['property.unit.sequence'].search([('unit_id', '=', record.id)], limit=1)
#             seq.sequence += 1  # incremental of the number
#             return f"{record.name}/{seq.sequence:04d}"
#
#     @api.onchange('contract_id')
#     def _onchange_contract_id(self):
#         self.date_from = self.contract_id.date_start
#         self.date_to = self.contract_id.date_end

    # @api.depends('unit_bld_code', 'number')
    # def _compute_display_nam(self):
    #
    #     if self.unit_bld_code:
    #         self.display_nam = self.unit_bld_code + '-' + self.number
    #     else:
    #         self.display_nam = False

class PropertyUnit(models.Model):
    _name = 'property.unit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Unit Details'
    _rec_name = 'display_name'
    # blank = '000'

    display_name = fields.Char('Name',compute='_compute_display_name',store=True)  # blank = '000' or building, compound => referenced property
    number = fields.Char('Unit Number')  # blank = '000' or building, compound => referenced property
    property_id = fields.Many2one(comodel_name='property.property',)  # blank = '000' or building, compound => referenced property
    type_id = fields.Many2one(comodel_name='property.type', string='Unit Type')
    bld_code = fields.Char(related='property_id.bld_code',store=True,string='Related Property Code')#compute='_compute_bld_code'
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='Valid Till')
    ra_no = fields.Char(string='RA NO')

    claim_ids = fields.One2many('claim.request', 'claim_no', string='Claim Requests')
    # asset_ids = fields.One2many('property.asset', 'asset_no', string='Assets')
    is_furnitured = fields.Selection([('furnitured', 'Furnitured'),('semi_furnitured', 'Semi Furnitured'), ('unfurnitured', 'Unfurnitured')])
    is_electric = fields.Selection([('electricity_water', 'Electricity And Water'),('no', 'No Electricity And Water')],string='Electric&Water')
    is_ac = fields.Selection([('ac', 'AC'),('no', 'No AC')],string='AC')

    ar_description = fields.Text('Unit Description')
    en_description = fields.Text('English Description')
    ar_address = fields.Char('Arabic Address')
    ar_address1 = fields.Char('Arabic Address1')
    en_address = fields.Char('English Address')
    en_address2 = fields.Char('English Address2')
    ar_city = fields.Char('Arabic City')

    # owner_id = fields.Many2one('property.owner', string='Owner Name')


    bedroom = fields.Char(string='Bedrooms')
    bathroom = fields.Char(string='Bathrooms')
    water_no = fields.Char(string='Water No')
    water_no1 = fields.Char(string='2nd Water No')
    kahrma_no = fields.Char(string='kahrma No')
    kahrma_no1 = fields.Char(string='2nd kahrma No')

    idle_rent = fields.Float(string='Ideal Rent (QR)',default=0.0,
        digits='Product Price',
        help="Ideal Rent Price")  # Monetory

    current_rent = fields.Float(string='Current Rent (QR)',default=0.0,
        digits='Product Price',
        help="Price at which the Property is Rented to Tenants.")  # Monetory
    is_occupied = fields.Selection([('occupied','Occupied'),('vacant','Vacant'),('allocated','Allocated'),],string='Occupied/Vacant/Allocated')

    contract_id = fields.Many2one('res.partner', string='Related Contracts')
    # =================================
    # =======Unit SEQUENCE=============
    # =================================
    sequence_ids = fields.One2many('property.unit.sequence', 'unit_id', string='Sequences')
    # company_id = fields.Many2one('res.company')

    @api.model
    def create(self, vals):
        record = super(PropertyUnit, self).create(vals)
        self.env['property.unit.sequence'].create({'unit_id': record.id})
        return record

    def generate_sequence(self):
        for record in self:
            seq = self.env['property.unit.sequence'].search([('unit_id', '=', record.id)], limit=1)
            seq.sequence += 1 # incremental of the number
            return f"{record.display_name}/{seq.sequence:04d}"

    @api.onchange('contract_id')
    def _onchange_contract_id(self):
        self.date_from = self.contract_id.date_start
        self.date_to = self.contract_id.date_end

    @api.depends('bld_code','number')
    def _compute_display_name(self):
        if self.bld_code:
            self.display_name = self.bld_code +'-'+ self.number
        else:
            self.display_name = False


class PropertyUnitType(models.Model):
    _name = 'unit.type'
    _description = 'Unit Type'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=False, )
    Description = fields.Char(string="Name", required=False, )


class PropertyUnitSequence(models.Model):
    _name = 'property.unit.sequence'
    _description = 'Property Unit Sequence'

    unit_id = fields.Many2one('property.unit', string='Property Unit', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
