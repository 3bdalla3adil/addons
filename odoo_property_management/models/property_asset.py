from odoo import models, fields


class PropertyAsset(models.Model):
    _name = 'property.asset'
    # _inherit = 'res.partner'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Asset Details'
    _rec_name = 'unit'

    unit = fields.Many2one('property.unit', 'Related Unit Number', required=True)

    name = fields.Char('Asset Name')
    description = fields.Text('Asset Description')
    count = fields.integer('Asset Count')


