from odoo import models, fields, api


# MEDICATION BODY MARKS HISTORY
class MedicalBodyMarkerHistory(models.Model):
    _name = "medical.body.markers.history"
    _description = "Medical Body Marker History"

    name = fields.Text('Markers Coordinate')
    appointment_id = fields.Many2one('medical.appointment')


# MEDICATION NOTES HISTORY
class MedicalNotesHistory(models.Model):
    _name = "medical.notes.history"
    _description = "Medical Note History"

    appointment_id = fields.Many2one('medical.appointment')
    user_id = fields.Many2one('res.users')
    last_notes = fields.Text('Previous Notes')
    update_notes = fields.Text('Updated Notes')


# MEDICATION MARKS HISTORY
class MedicalMarkerHistory(models.Model):
    _name = "medical.markers.history"
    _description = "Medical Marker History"

    name = fields.Text('Markers Coordinate')
    appointment_id = fields.Many2one('medical.appointment')



# FACE ORDER LINE
class FaceOrderLine(models.Model):
    _name = "face.order.line"
    _description = "Face Order Line"
    _order = "id desc"

    appointment_id = fields.Many2one('medical.appointment')
    product_id = fields.Many2one('product.product', string="Material", domain=[('is_material', '=', True)])
    quantity = fields.Float(string="Quantity", default=1)
    unit_price = fields.Float(string="Unit Price")
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal')

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.unit_price = rec.product_id.lst_price

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.unit_price * rec.quantity

# BODY ORDER LINE
class BodyOrderLine(models.Model):
        _name = "body.order.line"
        _description = "Body Order Line"
        _order = "id desc"

        appointment_id = fields.Many2one('medical.appointment')
        product_id = fields.Many2one('product.product', string="Material", domain=[('is_material', '=', True)])
        quantity = fields.Float(string="Quantity", default=1)
        unit_price = fields.Float(string="Unit Price")
        subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal')

        @api.onchange('product_id')
        def onchange_product_id(self):
            for rec in self:
                if rec.product_id:
                    rec.unit_price = rec.product_id.lst_price

        @api.depends('quantity', 'unit_price')
        def _compute_subtotal(self):
            for rec in self:
                rec.subtotal = rec.unit_price * rec.quantity
