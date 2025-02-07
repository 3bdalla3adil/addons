# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


# ===========================================================================================================
# ==== PIPELINE ============  Property Details ==> res.partner    =========================================
# ==========================  Building Details ==>                  =========================================
# ==========================  Unit     Details ==>                  =========================================
# ===========================================================================================================


#================================================================
#ToDo:Craft custom property ==> integrate with product
#================================================================

# class Partner(models.Model):
#     _inherit = 'res.partner'
#
#     _description = 'Property Details'
#     _rec_name = 'display_name'
#
#     # code = 'ab-01'
#     # owner
#     # reference = fields.Reference(selection="[('property.property', 'Property Code'), ('property.unit', 'Unit Number')]",string="Reference")
#
#     # bld_id = fields.Many2one('property.building', string='Property N')
#     # display_nam = fields.Char('Name', compute='_compute_display_nam',
#     #                           store=True)
#
#     bld_code = fields.Char(string='Property N', )
#     # no_of_units  = fields.Char('Number of Units')
#     bld_unit = fields.One2many('property.unit', 'property_id', string='Units N', )  #
#     bld_location = fields.Char(string='Building Location')
#     bld_type_id = fields.Many2one(comodel_name="property.type", string="Property Type", required=False, )
#     bld_url = fields.Char('Google Link')


class Property(models.Model):
    _name = 'property.property'
    # _inherit = 'product.product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _description = 'Property Details'
    _rec_name = 'bld_code'

    # code = 'ab-01'
    # owner
    # reference = fields.Reference(selection="[('property.property', 'Property Code'), ('property.unit', 'Unit Number')]",string="Reference")

    # bld_id = fields.Many2one('property.building', string='Property N')

    bld_code = fields.Char(string='Property N', )
    # no_of_units  = fields.Char('Number of Units')
    bld_unit = fields.One2many('property.unit', 'property_id', string='Units N', )  #
    bld_location = fields.Char(string='Building Location')
    bld_type_id = fields.Many2one(comodel_name="property.type", string="Property Type", required=False, )
    bld_url = fields.Char('Google Link')

    water_no = fields.Char(string='Water No')
    water_no1 = fields.Char(string='2nd Water No')
    kahrma_no = fields.Char(string='kahrma No')
    kahrma_no1 = fields.Char(string='2nd kahrma No')

    # owner_id   = fields.Char(related='bld_unit.owner_id', string='Owner Name')


class PropertyType(models.Model):
    _name = 'property.type'
    _description = 'Property Type'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=False, )
    Description = fields.Char(string="Name", required=False, )

    # @api.onchange
    # def _compute_unit_no(self):
    #     for rec in self:
    #         unit_no = rec.ref_no.split('-')[-1]
    #         rec.unit_no = unit_no

    # @api.model_create_multi
    # def create(self, vals_list):
    #     """ Create a sequence for the property model """
    #     for vals in vals_list:
    #         if vals.get('ref_no', _('New')) == _('New'):
    #             vals['ref_no'] = ()
    #     return super().create(vals_list)
