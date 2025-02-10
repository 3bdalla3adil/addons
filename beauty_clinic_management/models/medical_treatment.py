from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

# DONE
class MedicalTreatmentOrder(models.Model):
    _description = "Medical Treatment"
    _inherit = "repair.order"

    # ToDo: Should assign patient appointment only
    @api.depends('patient_id')
    @api.onchange('patient_id')
    def _compute_appointment(self):
        for rec in self:
            appt = [appt_id for appt_id in rec.patient_id.apt_id.ids if appt_id]
            rec.appt_ids = [(6, 0, appt)]
            #_logger.info(f"rec appointments {rec.appt_ids} appt is {appt}")

    # ToDo: Should list patient services only
    @api.depends('appt_ids')
    def _compute_service(self):
        for rec in self:
            rec.services = [(6, 0, [service.id for service in rec.appt_id.services_ids if
                                    service])]

            #_logger.info(f"rec services {rec.services} service is {rec.appt_ids}")

    #     def name_search(self, name, args=None, operator='ilike', limit=100):
    #         x = super(medical_teeth_treatment, self).name_search(self)
    #         return x

    #     def name_get(self):
    #         x = super(medical_teeth_treatment, self).name_get()
    #         return x

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        user = self.env.user.name
        if view_type == 'form' :#and user != 'ISMAIL':
            for node in arch.xpath("//field[@name='name']"):
                # node.set('invisible', '1')
                node.set('string', 'Treatment Reference')
            for node in arch.xpath("//page[@name='parts']"):
                node.set('string', 'Treatment Medicine')
                #node.set('widget', 'selection')
        #if view_type == 'tree' :and user == 'ISMAIL':
            for node in arch.xpath("//field[@name='product_id']"):
                node.set('string', 'Service')
            for node in arch.xpath("//field[@name='partner_id']"):
                node.set('string', 'Patient')
            for node in arch.xpath("//button[@name='action_repair_cancel']"):
                node.set('string', 'Cancel Treatment')
            for node in arch.xpath("//button[@name='action_repair_start']"):
                node.set('string', 'Confirm Treatment')
            for node in arch.xpath("//field[@name='picking_id']"):
                node.set('invisible', '1')
            for node in arch.xpath("//field[@name='under_warrenty']"):
                node.set('invisible', '1')
        return arch, view

    state = fields.Selection([
        ('draft', 'New'),
        ('confirmed', 'Confirmed'),
        ('under_repair', 'Under Treatment'),
        ('done', 'Finished Treatment'),
        ('cancel', 'Cancelled')], string='Status',
        copy=False, default='draft', readonly=True, tracking=True, index=True,
        help="* The \'New\' status is used when a user is encoding a new and unconfirmed Treatment order.\n"
             "* The \'Confirmed\' status is used when a user confirms the Treatment order.\n"
             "* The \'Under Treatment\' status is used when the treatment is ongoing.\n"
             "* The \'Finished\' status is set when Treatment is completed.\n"
             "* The \'Cancelled\' status is used when user cancel Treatment order.")

    treatment_no = fields.Char(string='Treatment No', default=lambda self: _('New'))

    treatment_type_id = fields.Many2one('medical.treatment.type', string='Type', )
    treatment_type = fields.Char(related='treatment_type_id.name', string='Type name', )

    patient_id = fields.Many2one('medical.patient', string='Patients')

    # state = fields.Selection([
    #     ('planned', 'Planned'),
    #     ('condition', 'Condition'),
    #     ('completed', 'Completed'),
    #     ('in_progress', 'In Progress'),
    #     ('invoiced', 'Invoiced')], 'Status', default='planned')

    doctor = fields.Many2one('medical.doctor', 'Doctor')
    user_id = fields.Many2one('res.users', 'Log In User', readonly=True, default=lambda self: self.env.user)
    appt_id = fields.Many2one('medical.appointment', string='Appointment ID')
    appt_ids = fields.Many2many('medical.appointment', 'patient_appt_rel', 'patient_id', 'appt_id',
                                compute='_compute_appointment', string='Appointments')
    equipment_id = fields.Many2one('medical.equipment', 'Equipment')
    treatment_line_ids = fields.One2many('medical.treatment.line', 'treatment_id')

    # MAIN TREATMENT INFORMATION
    # service = fields.Many2one('product.product', string='Service', domain=[('is_treatment', '=', True)])
    service = fields.Many2one('product.product', string='Service', domain=[('is_treatment', '=', True)])
    services = fields.Many2many('product.product', compute='_compute_service', string='Services', )
    amount = fields.Float(related='service.lst_price', string='Amount')
    treatment_area = fields.Text('Treatment Area')

    date = fields.Date(default=fields.Date.today, string='Date')
    remarks = fields.Text('Remarks')

    def notify_the_world(self, vals):
        users = self.env['res.users'].search(
            [('user_id', '!=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)])
        if 'state' in vals:
            state = vals['state']
            for treatment in self:
                for user in users:
                    user.notify_success(
                        f"A Treatment For Patient [{treatment.patient_id.patient_id}] have been Made Successfully.")

    # Create Serial No for Treatment
    # @api.model
    # def create(self, vals):
    #
    #     if vals.get('treatment_no', 'New') == 'New':
    #         vals['treatment_no'] = self.env['ir.sequence'].next_by_code('medical.treatment') or 'New'
    #     result = super(MedicalTreatment, self).create(vals)
    #     return result


class MedicalTreatment(models.Model):
    _description = "Medical Treatment"
    _name = "medical.treatment"

    _rec_name = "treatment_no"

    # ToDo: Should assign patient appointment only
    @api.depends('patient_id')
    @api.onchange('patient_id')
    def _compute_appointment(self):
        for rec in self:
            appt = [appt_id for appt_id in rec.patient_id.apt_id.ids if appt_id]
            rec.appt_ids = [(6, 0, appt)]
            _logger.info(f"rec appointments {rec.appt_ids} appt is {appt}")


    # ToDo: Should list patient services only
    @api.depends('appt_ids')
    def _compute_service(self):
        for rec in self:
            rec.services = [(6, 0, [service.id for service in rec.appt_id.services_ids if
                                    service])]

            _logger.info(f"rec services {rec.services} service is {rec.appt_ids}")
    #     def name_search(self, name, args=None, operator='ilike', limit=100):
    #         x = super(medical_teeth_treatment, self).name_search(self)
    #         return x

    #     def name_get(self):
    #         x = super(medical_teeth_treatment, self).name_get()
    #         return x

    treatment_no = fields.Char(string='Treatment No', default=lambda self: _('New'))

    treatment_type_id = fields.Many2one('medical.treatment.type', string='Type', )
    treatment_type = fields.Char(related='treatment_type_id.name', string='Type name', )

    patient_id = fields.Many2one('medical.patient', string='Patients')

    state = fields.Selection([
        ('planned', 'Planned'),
        ('condition', 'Condition'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('invoiced', 'Invoiced')], 'Status', default='planned')

    doctor = fields.Many2one('medical.doctor', 'Doctor')
    user_id = fields.Many2one('res.users', 'Log In User', readonly=True, default=lambda self: self.env.user)
    appt_id = fields.Many2one('medical.appointment', string='Appointment ID')
    appt_ids = fields.Many2many('medical.appointment', 'patient_appt_rel', 'patient_id', 'appt_id',
                                compute='_compute_appointment', string='Appointments')
    equipment_id = fields.Many2one('medical.equipment', 'Equipment')
    treatment_line_ids = fields.One2many('medical.treatment.line', 'treatment_id')

    # MAIN TREATMENT INFORMATION
    # service = fields.Many2one('product.product', string='Service', domain=[('is_treatment', '=', True)])
    service = fields.Many2one('product.product', string='Service', domain=[('is_treatment', '=', True)])
    services = fields.Many2many('product.product', compute='_compute_service', string='Services', )
    amount = fields.Float(related='service.lst_price', string='Amount')
    treatment_area = fields.Text('Treatment Area')

    date = fields.Date(default=fields.Date.today, string='Date')
    remarks = fields.Text('Remarks')

    def notify_the_world(self, vals):
        users = self.env['res.users'].search(
            [('user_id', '!=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)])
        if 'state' in vals:
            state = vals['state']
            for treatment in self:
                for user in users:
                    user.notify_success(
                        f"A Treatment For Patient [{treatment.patient_id.patient_id}] state have Made Successfully.")

    # Create Serial No for Treatment
    @api.model
    def create(self, vals):

        if vals.get('treatment_no', 'New') == 'New':
            vals['treatment_no'] = self.env['ir.sequence'].next_by_code('medical.treatment') or 'New'
        result = super(MedicalTreatment, self).create(vals)
        return result


class MedicalTreatmentLine(models.Model):
    _description = "Medical Treatment Line"
    _name = "medical.treatment.line"

    # MAIN TREATMENT INFORMATION
    treatment_no = fields.Char(related='treatment_id.treatment_no', string='Treatment No', )
    treatment_id = fields.Many2one(comodel_name='medical.treatment', string='Treatment ID', )
    patient_id = fields.Many2one(comodel_name='medical.patient', compute='_compute_patient_id', store=True,
                                 string='Patient ID')

    treatment_type = fields.Char(related='treatment_id.treatment_type', string='treatment type', )

    treatment_area = fields.Text(related='treatment_id.treatment_area', string='Treatment Area', store=True)
    state = fields.Selection(
        [('planned', 'Planned'),
         ('condition', 'Condition'),
         ('completed', 'Completed'),
         ('in_progress', 'In Progress'),
         ('invoiced', 'Invoiced')], 'Status', default='planned')
    doctor = fields.Many2one(comodel_name='medical.doctor',
                             compute='_compute_doctor_id', string='Nurse/Doctor', store=True)
    date = fields.Date(default=fields.Date.today, string='Date')
    remarks = fields.Text(related='treatment_id.remarks', string='Remarks')

    # SCARLET
    forehead = fields.Char(string='ForeHead')
    per_orbital = fields.Char(string='Per Orbital')
    nose_upper = fields.Char(string='Nose/Upper Lip/Chin')
    cheeks = fields.Char(string='Cheeks')

    # PROCEDURE
    procedure = fields.Char(string='Procedure')

    # LASER
    length = fields.Char(string='Wave/Length')
    fluence = fields.Char(string='Fluence/')
    pulse = fields.Char(string='Pulse Width')
    hand_piece = fields.Char('Hand Piece')

    #HiFU
    cartridge = fields.Char(string='Cartridge')
    power = fields.Char(string='Shot Per Cartridge')
    pitch = fields.Char(string='Pitch')

    @api.depends('treatment_id')
    def _compute_doctor_id(self):
        for rec in self:
            rec.doctor = rec.treatment_id.doctor.id

    @api.depends('treatment_id')
    def _compute_patient_id(self):
        for rec in self:
            if rec.treatment_id.patient_id:
                rec.patient_id = rec.treatment_id.patient_id.id


class MedicalTreatmentType(models.Model):
    _name = 'medical.treatment.type'
    _description = 'Medical Treatment type'

    name = fields.Char('Name')
    description = fields.Text('Description')
