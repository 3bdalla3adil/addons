from odoo import models, fields, api, _

import logging
from datetime import datetime, timedelta, time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
import pytz

_logger = logging.getLogger(__name__)


# APPOINTMENT
class MedicalAppointment(models.Model):
    _name = "medical.appointment"
    _description = "Medical Appointment"
    # _rec_name = "complete_name"
    _order = "appointment_sdate desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ADD added service duration to whole appointment time

    # =====================USE WEB NOTIFY MODULE==========================================
    def update_screen(self):
        pass
        # for record in self:
        #     import json
        #     self.env['bus.bus'].sendone(
        #         (self._cr.dbname, 'medical.appointment', record.id),
        #         json.dumps({'type': 'refresh', 'model_name': 'medical.appointment', 'rec_id': record.id})
        #     )

    @api.model
    def write(self, vals):
        result = super(MedicalAppointment, self).write(vals)
        # Publish the event to the bus
        self.update_screen()
        return result

    @api.onchange('services_ids')
    def services_timeadd(self):
        dt = datetime.strptime(str(self.appointment_sdate), '%Y-%m-%d %H:%M:%S')
        server_time = dt + timedelta(hours=5, minutes=30)
        val = []
        for ids in self.services_ids.ids:
            val.append(ids)
        service_time = self.env['product.product'].search([('id', '=', val)])
        main = []
        for service in service_time:
            main.append(service.duration_id.duration_name)
        minute = sum(main)
        end_time = server_time + timedelta(minutes=minute)
        self.appointment_edate = end_time - timedelta(hours=5, minutes=30)
        self.update_screen()

    # Notify Users that Service changes
    def notify_the_world(self, vals):
        users = self.env['res.users'].search(
            [('user_id', '!=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)])
        if 'state' in vals:
            state = vals['state']
            for appointment in self:
                for user in users:
                    user.notify_warning(
                        f"Appointment For Patient [{appointment.patient.patient_id}] state has been changed to {state}.")
        self.update_screen()

        # notification_ids = []
        # if users:
        #     notification_ids = [(0, 0,
        #                          {
        #                              'res_partner_id': user.partner_id.id,
        #                              'notification_type': 'inbox'
        #                          }
        #                          ) for user in users if users]
        # if 'state' in vals:
        #     for appointment in self:
        #         self.env['mail.message'].create({
        #             'message_type': "notification",
        #             'body': f"The appointment patient [{
        #             appointment.patient.patient_id}] state has been changed to {vals["state"]}.",
        #             'subject': "Appointment Status Update!",
        #             'partner_ids': [(4, user.partner_id.id) for user in users if users],
        #             'model': self._name,
        #             'res_id': self.id,
        #             'notification_ids': notification_ids,
        #             'author_id': self.env.user.partner_id and self.env.user.partner_id.id
        #         })

    @api.model
    def write(self, vals):
        self.notify_the_world(vals)
        return super(MedicalAppointment, self).write(vals)

    # DONE
    @api.onchange('appointment_sdate', 'clinic')
    def appointment_validation(self):
        validation = self.search([
            ('clinic', '=', self.clinic.id),
            ('appointment_sdate', '>=', self.appointment_sdate),
        ])
        if validation:
            raise ValidationError("Already Booked The Appointment")
        else:
            pass

    # DONE
    def edit_appointment(self, event_id):
        appointment_id = self.search([('id', '=', event_id)], limit=1)
        if appointment_id:
            context = dict(self.env.context)
            tz = self.env.user.tz
            # tz = 'Asia/Qatar'
            tz = pytz.timezone(tz)
            from_time_tz = pytz.utc.localize(appointment_id.appointment_sdate).astimezone(tz)
            from_time = from_time_tz.strftime('%H:%M')
            split_data = from_time.split(':')

            to_time_tz = pytz.utc.localize(appointment_id.appointment_edate).astimezone(tz)
            to_time = to_time_tz.strftime('%H:%M')
            to_split_data = to_time.split(':')

            vals = {
                'appointment_sdate': appointment_id.appointment_sdate,
                'appointment_edate': appointment_id.appointment_edate,
                'appointment_id': appointment_id.id,
                'doctor_id': appointment_id.doctor.id,
                'clinic': appointment_id.clinic.id,
                'mobile_number': appointment_id.patient.mobile,
                'patient_id': appointment_id.patient.id,
                'service_ids': [(6, 0, appointment_id.services_ids.ids)],
                'from_time': (float(split_data[0]) * 60 + float(split_data[1])) / 60,
                'to_time': (float(to_split_data[0]) * 60 + float(to_split_data[1])) / 60,
            }
            caw_id = self.env['calender.appointment.wizard'].create(vals)
            self.update_screen()
            return caw_id.id

    # DONE
    def check_appointment(self, event_name):
        record = self.search([('name', '=', event_name)], limit=1)
        app_ids = self.search([
            ('id', '!=', record.id),
            ('clinic', '=', record.clinic.id),
            ('appointment_sdate', '>=', record.appointment_sdate),
            ('appointment_edate', '<=', record.appointment_edate)
        ])
        if app_ids:
            return True
        else:
            return False

    # Added Service
    # GET APPOINTMENT RESERVATION BASED ON name and clinic_id # DONE
    def get_data(self, clinic, event_name, index):
        record = self.search([('name', '=', event_name), ('clinic', '=', clinic)], limit=1)
        #_logger.info("===============Services=============={}".format('+'.join(service.name for service in record.services_ids if service)))
        if record:
            return {
                'index': index, 'patient': record.patient.partner_id.name,'clinic': record.clinic.name,
                'service': '{}'.format('+'.join(service.name for service in record.services_ids)),
                'state': record.state, 'patient_id': record.patient.patient_id
            }
        else:
            return {
                'index': 0, 'patient': record.patient.partner_id.name,'clinic': record.clinic.name,
                'service': '{}'.format('+'.join(service.name for service in record.services_ids)),
                'state': record.state, 'patient_id': record.patient.patient_id
            }

    # Done!
    @api.model
    def _get_default_doctor(self):
        doc_ids = None
        partner_ids = [x.id for x in
                       self.env['res.partner'].search([('user_id', '=', self.env.user.id), ('is_doctor', '=', True)])]
        if partner_ids:
            doc_ids = [x.id for x in self.env['medical.doctor'].search([('name', 'in', partner_ids)])]
        return doc_ids

    # DONE
    @api.model
    def _get_default_clinic(self):
        clinic_ids = None
        partner_ids = [x.id for x in
                       self.env['res.partner'].search([('is_clinic', '=', True)])]
        if partner_ids:
            clinic_ids = [x.id for x in self.env['medical.clinic'].search([('name', 'in', partner_ids)])]
        return clinic_ids

    def delayed_time(self):
        result = {}
        for patient_data in self:
            if patient_data.checkin_time and patient_data.checkin_time > patient_data.appointment_sdate:
                self.delayed = True
            else:
                self.delayed = False

    @api.onchange('duration_id', 'appointment_sdate')
    def delayed_duration(self):
        if self.duration_id and self.appointment_sdate:
            self.appointment_edate = self.appointment_sdate + timedelta(minutes=self.duration_id.duration_name)

    def _waiting_time(self):
        def compute_time(checkin_time, ready_time):
            now = datetime.now()
            if checkin_time and ready_time:
                ready_time = datetime.strptime(str(ready_time), '%Y-%m-%d %H:%M:%S')
                checkin_time = datetime.strptime(str(checkin_time), '%Y-%m-%d %H:%M:%S')
                delta = relativedelta(ready_time, checkin_time)
                years_months_days = str(delta.hours) + "h " + str(delta.minutes) + "m "
            else:
                years_months_days = "No Waiting time !"

            return years_months_days

        for patient_data in self:
            patient_data.waiting_time = compute_time(patient_data.checkin_time, patient_data.ready_time)

    active = fields.Boolean(default="True")
    allday = fields.Boolean('All Day', default=False)

    operations = fields.One2many('medical.treatment', 'appt_id', 'Operations')
    clinic = fields.Many2one('medical.clinic', 'Clinic', help="Clinic's Name", required=True,
                             default=_get_default_clinic)
    name = fields.Char('Appointment ID', size=64, readonly=True, default=lambda self: _('New'))
    patient = fields.Many2one('medical.patient', 'Patient', help="Patient Name", required=True, )
    appointment_sdate = fields.Datetime('Appointment Start', required=True, default=fields.Datetime.now)
    appointment_edate = fields.Datetime('Appointment End', required=True, )
    cancel_reason = fields.Text('Cancel Reason', )
    # DONE
    doctor = fields.Many2one('medical.doctor', 'Doctor', required=False, )
    urgency = fields.Boolean('Urgent', default=False)
    comments = fields.Text('Note', )
    checkin_time = fields.Datetime('Checkin Time', readonly=True, )
    ready_time = fields.Datetime('In Chair', readonly=True, )
    waiting_time = fields.Char('Waiting Time', compute='_waiting_time')
    no_invoice = fields.Boolean('Invoice exempt')
    invoice_done = fields.Boolean('Invoice Done')
    user_id = fields.Many2one('res.users', related='clinic.user_id', string='clinic', store=True)
    inv_id = fields.Many2one('account.move', 'Invoice', readonly=True)
    state = fields.Selection(
        # [('draft', 'Unconfirmed'), ('arrived', 'Arrived'), ('confirmed', 'Confirmed'), ('missed', 'Missed'),
        # [('draft', 'Unconfirmed'), ('confirmed', 'Confirmed'), ('missed', 'Missed'),
        [('draft', 'Unconfirmed'), ('confirmed', 'Arrived'), ('missed', 'Missed'),
         ('checkin', 'Checked In'), ('ready', 'In Chair'), ('done', 'Completed'), ('cancel', 'Canceled')], 'State',
        readonly=True, default='draft')
    apt_id = fields.Boolean(default=False)
    apt_process_ids = fields.Many2many('medical.procedure', 'apt_process_rel', 'appointment_id', 'process_id',
                                       "Initial Treatment")
    pres_id1 = fields.One2many('medical.prescription.order', 'pid1', 'Prescription')
    patient_state = fields.Selection([('walkin', 'Walk In'), ('withapt', 'Come with Appointment')], 'Patients status',
                                     required=True, default='withapt')
    state_color = fields.Char(compute='_get_state_color', string='Color')
    #     treatment_ids = fields.One2many ('medical.lab', 'apt_id', 'Treatments')
    saleperson_id = fields.Many2one('res.users', 'Created By', default=lambda self: self.env.user)
    delayed = fields.Boolean(compute='delayed_time', string='Delayed', store=True)
    # service_id = fields.Many2one('product.product', 'Consultation Service')
    services_ids = fields.Many2many('product.product', 'apt_service_rel', 'appointment_id', 'service', 'Services')
    qid = fields.Char('QId', related="patient.qid")
    mobile = fields.Char('Mobile', related="patient.mobile")
    duration_id = fields.Many2one('duration.duration', 'Duration')
    payment_due = fields.Float(compute='_compute_payment_due', string='Payment Due')
    invoice_amount = fields.Float(compute='_compute_invoice_amount', string='Invoice Amount')
    invoice_amount_char = fields.Char(compute='_compute_invoice_amount', string='Invoice Amount')
    invoice_paid = fields.Float(compute='_compute_invoice_paid', string='Paid Amount')
    invoice_paid_char = fields.Char(compute='_compute_invoice_paid', string='Paid Amount')
    invoice_balance = fields.Float(compute='_compute_invoice_balance', string='Balance')
    invoice_balance_char = fields.Char(compute='_compute_invoice_balance', string='Balance')
    invoice_id = fields.Many2one('account.move')
    saleorder_id = fields.Many2one('sale.order')
    note_ids = fields.One2many('medical.notes.history', 'appointment_id', 'Notes History')
    marker_ids = fields.One2many('medical.markers.history', 'appointment_id', 'Face Markers History')
    body_marker_ids = fields.One2many('medical.body.markers.history', 'appointment_id', 'Body Markers History')
    face_order_line_ids = fields.One2many('face.order.line', 'appointment_id', 'Face Lines')
    body_order_line_ids = fields.One2many('body.order.line', 'appointment_id', 'Body Lines')
    treatment_note = fields.Text('Treatment Note Face', )
    treatment_body_note = fields.Text('Treatment Note Body', )
    complete_name = fields.Char(compute='_name_get_fnc', string="Name")

    face_material_usage_ids = fields.Many2many('product.product', 'apt_face_material_rel', 'appointment_id',
                                               'material_face_usage_id', 'Face Material usage',
                                               domain=[('is_material', '=', True)])
    body_material_usage_ids = fields.Many2many('product.product', 'apt_body_material_rel', 'appointment_id',
                                               'material_body_usage_id', 'Body Material usage',
                                               domain=[('is_material', '=', True)])

    invoice_state = fields.Selection(string="Invoice Status",
                                     selection=[('invoiced', 'Invoiced'), ('payment_registered', 'Payment Registered')])
    is_invoice_state = fields.Boolean(default=False)
    is_register_payment = fields.Boolean(default=False)

    def get_today(self):
        return fields.Date.today().strftime('%Y-%m-%d')

    def get_clinics(self):
        return self.env['medical.clinic'].search([], limit=5)

    def get_clinic_schedule(self):
        # Set up time range and clinics
        today = fields.Date.today()
        start_time = datetime.combine(today, datetime.strptime('09:00', '%H:%M').time())
        end_time = datetime.combine(today, datetime.strptime('20:00', '%H:%M').time())
        clinics = self.env['medical.clinic'].search([], limit=5)

        # Generate 30-minute time slots
        time_slots = []
        current_time = start_time
        while current_time < end_time:
            time_slots.append((current_time, current_time + timedelta(minutes=30)))
            current_time += timedelta(minutes=30)

        # Initialize schedule data structure
        schedule_data = {}
        for slot_start, slot_end in time_slots:
            slot_key = slot_start.strftime('%H:%M') + ' - ' + slot_end.strftime('%H:%M')
            schedule_data[slot_key] = {}

            # For each clinic, find appointments in the current slot
            for clinic in clinics:
                appointment = self.env['medical.appointment'].search([
                    ('clinic', '=', clinic.id),
                    ('appointment_sdate', '>=', slot_start),
                    ('appointment_sdate', '<', slot_end),
                    ('active', '=', True)
                ], limit=1)
                schedule_data[slot_key][clinic] = appointment if appointment else None

        return schedule_data

    # @api.model
    # def _name_get_fnc(self):
    #     for rec in self:
    #         if rec.patient:
    #             complete_name = rec.patient.partner_id.name
    #             if rec.appointment_sdate and rec.appointment_edate:
    #                 appointment_sdate = rec.appointment_sdate + timedelta(hours=5, minutes=30)
    #                 appointment_edate = rec.appointment_edate + timedelta(hours=5, minutes=30)
    #                 complete_name = complete_name + ' ' + str(appointment_sdate.time())[0:5] + ' to ' + str(
    #                     appointment_edate.time())[0:5]
    #             rec.complete_name = complete_name
    #         else:
    #             rec.complete_name = rec.name

    @api.model
    def _name_get_fnc(self):
        for rec in self:
            if rec.patient:
                complete_name = rec.patient.partner_id.name
                if rec.appointment_sdate and rec.appointment_edate:
                    appointment_sdate = rec.appointment_sdate + timedelta(hours=3)
                    # appointment_edate = rec.appointment_edate + timedelta(hours=5, minutes=30)
                    appointment_edate = rec.appointment_edate + timedelta(hours=3)
                    # complete_name = complete_name + ' ' + str(appointment_sdate.time())[0:5] + ' to ' + str(
                    #     appointment_edate.time())[0:5]
                    # complete_name = complete_name + '[' + rec.patient.patient_id + ']' + '{}'.format(
                    complete_name = complete_name + '[' + rec.clinic.name + ']' + '{}'.format(
                        '+'.join(service.name for service in rec.services_ids))
                rec.complete_name = complete_name
            else:
                rec.complete_name = rec.name + '[' + rec.clinic.name + ']' + '{}'.format(
                    '+'.join(service.name for service in rec.services_ids)),

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(MedicalAppointment, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                              submenu=submenu)
        return res

    def _compute_invoice_amount(self):
        for rec in self:
            ml_ids = self.env['account.move'].search(
                [('appointment_id', '=', rec.id), ('move_type', '=', 'out_invoice')])
            rec.invoice_amount = sum(ml_ids.mapped('amount_total'))
            rec.invoice_amount_char = "%.2f" % sum(ml_ids.mapped('amount_total'))

    def _compute_invoice_balance(self):
        for rec in self:
            ml_ids = self.env['account.move'].search(
                [('appointment_id', '=', rec.id), ('move_type', '=', 'out_invoice')])
            rec.invoice_balance = sum(ml_ids.mapped('amount_residual'))
            rec.invoice_balance_char = "%.2f" % sum(ml_ids.mapped('amount_residual'))

    @api.depends('invoice_amount', 'invoice_balance')
    def _compute_invoice_paid(self):
        for rec in self:
            rec.invoice_paid = rec.invoice_amount - rec.invoice_balance
            rec.invoice_paid_char = "%.2f" % (rec.invoice_amount - rec.invoice_balance)

    def _compute_payment_due(self):
        for rec in self:
            ml_ids = self.env['account.move'].search([
                ('partner_id', '=', rec.patient.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('amount_residual', '>', 0)])
            rec.payment_due = sum(ml_ids.mapped('amount_residual'))

    _sql_constraints = [
        ('date_check', "CHECK (appointment_sdate <= appointment_edate)",
         "Appointment Start Date must be before Appointment End Date !"), ]

    def get_date(self, date1, lang):
        new_date = ''
        if date1:
            search_id = self.env['res.lang'].search([('code', '=', lang)])
            new_date = datetime.strftime(datetime.strptime(date1, '%Y-%m-%d %H:%M:%S').date(), search_id.date_format)
        return new_date

    #====================================================================================================
    def done(self):
        self.update_screen()
        return self.write({'state': 'done'})

    # Reset to Draft
    def reset(self):
        return self.write({'state': 'draft'})

    # Cancel With Reason
    def cancel_appointment(self):
        self.cancel()

        return {
            'name': _('Cancel'),
            'view_mode': 'form',
            'res_model': 'cancel.reason',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_id': self.env.ref('beauty_clinic_management.cancel_reason_wizard').id,
            'context': {'default_appointment_id': self.id},
        }

    def cancel(self):
        self.update_screen()
        return self.write({'state': 'cancel'})

    def confirm_appointment(self):
        self.update_screen()
        return self.write({'state': 'confirmed'})

    def send_state(self):
        return self.write({'state': 'sms_send'})

    def confirm(self):
        self.update_screen()
        for rec in self:
            appt_end_date = rec.appointment_edate
            attandee_ids = []
            attandee_ids.append(rec.patient.partner_id.id)
            # Related Clinic Attend
            attandee_ids.append(rec.clinic.res_partner_medical_clinic_id.id)
            attandee_ids.append(3)
            if not rec.appointment_edate:
                appt_end_date = rec.appointment_sdate
            self.env['calendar.event'].create(
                {'name': rec.name,
                 'partner_ids': [[6, 0, attandee_ids]],
                 'start': rec.appointment_sdate,
                 'stop': appt_end_date, })
        self.write({'state': 'confirmed'})

    def sms_send(self):
        return self.write({'state': 'sms_send'})

    def ready(self):
        now = datetime.now()
        # ready_time = time.strftime('%Y-%m-%d %H:%M:%S')
        ready_time = now.strftime('%Y-%m-%d %H:%M:%S')  #changed time to now
        self.write({'state': 'ready', 'ready_time': ready_time})
        self.update_screen()
        return True

    def missed(self):
        self.write({'state': 'missed'})
        self.update_screen()

    def checkin(self):

        now = datetime.now()
        # checkin_time = time.strftime('%Y-%m-%d %H:%M:%S')
        checkin_time = now.strftime('%Y-%m-%d %H:%M:%S')  #changed time to now
        self.write({'state': 'checkin',
                    'checkin_time': checkin_time})
        self.update_screen()

    # SET COLOR BASED ON STATUS
    #=============================================================================================
    def _get_state_color(self):
        state_color_map = {
            'draft': '#F8F842',  # LightYellow
            # 'sms_send': '#FFDAB9',  # LightOrange
            'confirmed': '#FE9900',  # Orange
            'missed': '#F953CF', #
            'checkin': '#ADD8E6',  # LightBlue
            'ready': '#DDA0DD',  # LightPurple(Indigo)
            'cancel': '#FB7171',  # LightRed
            'done': '#7AFF45',  # LightGreen
        }

        for record in self:
            record.state_color = state_color_map.get(record.state, '#FFFFFF')  # default to white

    # =============================================================================================
    # def _get_datas(self, start_datetime, end_datetime):
    #     """Get a mapping from partner id to attended events intersecting with the time interval.
    #
    #     :return dict[int, <medical.appointment>]:
    #     """
    #     events = self.search([
    #         ('appointment_sdate', '>=', start_datetime),
    #         ('appointment_sdate', '<=', end_datetime),
    #     ])
    #
    #     from collections import defaultdict
    #     event_by_partner_id = defaultdict(lambda: self.env['medical.appointment'])
    #     for event in events:
    #         event_by_partner_id[event.partner_id.id] += event
    #
    #     return dict(event_by_partner_id)
    # =============================================================================================
    # DONE
    def _prepare_invoice(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'narration': self.comments,
            'invoice_user_id': self.saleperson_id and self.saleperson_id.id,
            'partner_id': self.patient.partner_id.id,
            'invoice_line_ids': [],
            'clinic': self.clinic.id,
            'doctor': self.doctor.id,  # APPROVED
            'invoice_date': datetime.today()
        }
        return invoice_vals

    # clinic.id DONE!
    def create_invoices(self):
        invoice_vals = self._prepare_invoice()
        for line in self.operations:
            res = {}
            res.update({
                # 'name': line.description.name,
                # 'product_id': line.description.id,
                'product_id': line.service.id,
                'price_unit': line.amount,
                'quantity': 1.0,
            })
            invoice_vals['invoice_line_ids'].append((0, 0, res))
        if self.services_ids:
            for line in self.services_ids:
                res = {}
                res.update({
                    # 'name': line.description.name,
                    # 'product_id': line.description.id,
                    'product_id': line.id,
                    'price_unit': line.lst_price,
                    'quantity': 1.0,
                })
                invoice_vals['invoice_line_ids'].append((0, 0, res))
        inv_id = self.env['account.move'].create(invoice_vals)
        if inv_id:
            self.inv_id = inv_id.id
            self.invoice_done = True
        self.update_screen()
        return inv_id

    #DONE!
    def register_payment(self):

        pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                       active_ids=self.inv_id.ids).create(
            {
                'payment_date': self.inv_id.invoice_date,
                'journal_id': self.inv_id.journal_id.id,
                'amount': self.inv_id.amount,
                'payment_method_line_id': self.inv_id.journal_id.payment_method_line_id.id,
            })
        pmt_wizard._create_payments()
        message_id = self.env['medical.notes.message'].create({'name': _("Payment successfully created.")})
        self.update_screen()
        return {
            'name': _('Success'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'medical.notes.message',
            'res_id': message_id.id,
            'target': 'new'
        }

    @api.model
    def create(self, vals):
        self.notify_the_world(vals)
        for appointmnet in self:
            if appointmnet.clinic.id == vals['clinic']:
                history_start_date = datetime.strptime(str(appointmnet.appointment_sdate), '%Y-%m-%d %H:%M:%S')
                history_end_date = False
                reservation_end_date = False
                if appointmnet.appointment_edate:
                    history_end_date = datetime.strptime(str(appointmnet.appointment_edate), '%Y-%m-%d %H:%M:%S')
                reservation_start_date = datetime.strptime(str(vals['appointment_sdate']), '%Y-%m-%d %H:%M:%S')
                #                 if vals.has_key('appointment_edate') and vals['appointment_edate']:
                if 'appointment_edate' in vals and vals['appointment_edate']:
                    reservation_end_date = datetime.strptime(str(vals['appointment_edate']), '%Y-%m-%d %H:%M:%S')
                if history_end_date and reservation_end_date:
                    if (history_start_date <= reservation_start_date < history_end_date) or (
                            history_start_date < reservation_end_date <= history_end_date) or (
                            (reservation_start_date < history_start_date) and (
                            reservation_end_date >= history_end_date)):
                        raise ValidationError(
                            _('Clinic  %s is booked in this reservation period!') % appointmnet.clinic.name)
                elif history_end_date:
                    if (history_start_date <= reservation_start_date) or (
                            history_start_date < reservation_end_date) or (reservation_start_date < history_start_date):
                        raise ValidationError(
                            _('Clinic  %s is booked in this reservation period!') % appointmnet.clinic.name)
                elif reservation_end_date:
                    if (history_start_date <= reservation_start_date < history_end_date) or (
                            history_start_date <= history_end_date) or (reservation_start_date < history_start_date):
                        raise ValidationError(
                            _('Clinic  %s is booked in this reservation period!') % appointmnet.clinic.name)

            # DIMMED DOCTOR to MIGRATE to CLINIC
        #====================================================BEGIN===============================================================
        # if appointmnet.clinic.id == vals['clinic']:
        #     reservation_end_date = False
        #     history_end_date = False
        #     history_start_date = datetime.strptime(str(appointmnet.appointment_sdate), '%Y-%m-%d %H:%M:%S')
        #     if appointmnet.appointment_edate:
        #         history_end_date = datetime.strptime(str(appointmnet.appointment_edate), '%Y-%m-%d %H:%M:%S')
        #     reservation_start_date = datetime.strptime(str(vals['appointment_sdate']), '%Y-%m-%d %H:%M:%S')
        #     if vals['appointment_edate']:
        #         reservation_end_date = datetime.strptime(str(vals['appointment_edate']), '%Y-%m-%d %H:%M:%S')
        #     if (reservation_end_date and history_end_date) and (
        #             (history_start_date <= reservation_start_date < history_end_date) or (
        #             history_start_date < reservation_end_date <= history_end_date) or (
        #                     (reservation_start_date < history_start_date) and (
        #                     reservation_end_date >= history_end_date))):
        #         if appointmnet.clinic.id == vals['clinic']:
        #             raise ValidationError(
        #                 _('Clinic  %s is booked in this reservation period !') % (appointmnet.clinic.name.name))
        #======================================================END===============================================================
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('medical.appointment') or 'New'

        result = super(MedicalAppointment, self).create(vals)
        if result.patient and result.pres_id1:
            for prescription in result.pres_id1:
                if result.patient.id != prescription.name.id:
                    raise ValidationError(
                        "You cannot fill in the data of another patient in the prescription.\n"
                        "The prescription should have details of the patient defined in 'Patient' Field.")

        self._cr.execute('insert into pat_apt_rel(patient,apid) values (%s,%s)', (vals['patient'], result.id))
        return result


class AppointmentDuration(models.Model):
    _name = 'duration.duration'
    _description = 'Duration'
    _rec_name = 'duration_name'

    duration_name = fields.Integer(string='Duration')
    name = fields.Char(string='Name')
    # appointment_id = fields.Many2one('medical.appointment', string='Appointment')


class CancelReason(models.Model):
    _name = 'cancel.reason'
    _description = 'Cancel Reason'

    name = fields.Text('Reason')
    appointment_id = fields.Many2one('medical.appointment')

    def action_cancel(self):
        self.appointment_id.cancel_reason = self.name
