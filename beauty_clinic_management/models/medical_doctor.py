from odoo import models, fields, api, _



class MedicalDoctor(models.Model):
    _name = "medical.doctor"
    _description = "Medical Doctor Room"

    name = fields.Char(related='res_partner_medical_doctor_id.name', required=True, help='Name of the Operating Room')
    institution = fields.Many2one('res.partner', 'Institution', domain=[('is_institution', '=', True)],
                                  help='Medical Center')
    building = fields.Many2one('medical.hospital.building', string='Building', index=True)
    unit = fields.Many2one('medical.hospital.unit', string='Unit')
    extra_info = fields.Text('Extra Info')

    res_partner_medical_doctor_id = fields.Many2one('res.partner',string='Name')
    patient_id = fields.Many2one('medical.patient', string='Patient', )

    clinic_id = fields.Many2one('medical.clinic', string='Clinic', )
    equipment_ids = fields.One2many('medical.equipment', 'clinic', string='Equipments', )
    appointment_ids = fields.One2many('medical.appointment', 'doctor', string='Appointments', )
    procedure_ids = fields.Many2many('medical.procedure', string='Procedures', )

    doctor_slot_ids = fields.One2many('doctor.slot','doctor',copy=True, string='Availability', )

    active = fields.Boolean('Archive', default=True)
    active_code = fields.Char('ID', default='Test', compute='doctor_active', store=True)

    # Deactivate Non-active doctor based on appointment
    @api.depends('active_code', 'active')
    def doctor_active(self):
        for record in self:
            if record.active_code:
                if record.active_code and record.active == False:
                    doctor = self.env['medical.appointment'].sudo().search(
                        [('doctor.name', '=', record.name), ('active', '=', True)])
                    for doc in doctor:
                        doc.write({'active': False})
                if record.active_code and record.active == True:
                    doctor = self.env['medical.appointment'].sudo().search(
                        [('doctor.name', '=', record.name), ('active', '=', False)])
                    for doc in doctor:
                        doc.write({'active': True})



class DoctorSlot(models.Model):
    _name = 'doctor.slot'
    _description = 'doctor Slots'

    doctor = fields.Many2one('medical.doctor', string='doctor')
    weekday = fields.Selection([
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ], string='Week Day', required=True)
    start_hour = fields.Float('Starting Hour')
    end_hour = fields.Float('Ending Hour')


    @api.model
    def get_doctors_slot(self, target_date=False, doctor=False):
        from datetime import datetime
        if target_date:
            ask_time = datetime.strptime(target_date, "%a %b %d %Y %H:%M:%S %Z%z").date()
            weekday = ask_time.isoweekday()
        else:
            weekday = datetime.today().isoweekday()

        domain = [('weekday', '=', str(weekday))]
        if doctor:
            domain += [('doctor', '=', int(doctor))]
        slot_ids = sorted(self.search(domain), reverse=True)
        data_dict = {}
        for lt in slot_ids:
            doctor = lt.doctor
            start_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.start_hour * 60, 60))
            end_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.end_hour * 60, 60))
            if doctor.id not in data_dict and doctor.active:
                data_dict[doctor.id] = {
                    'id': doctor.id,
                    'name': doctor.res_partner_medical_doctor_id.name,
                    'count': 1,
                    'time_slots': [{'start_hour': start_hour, 'end_hour': end_hour}]
                }
            elif doctor.id in data_dict:
                data_dict[doctor.id].get('time_slots').append({'start_hour': start_hour, 'end_hour': end_hour})
                count = data_dict[doctor.id].get('count')
                data_dict[doctor.id].update({'count': count + 1})

        final_list = []
        for i in data_dict:
            final_list.append(data_dict.get(i))
        return final_list

    @api.model
    def get_doctors_slot_validation(self, target_date=False, doctor=False):
        from datetime import datetime
        if target_date:
            ask_time = datetime.strptime(target_date, "%a %b %d %Y %H:%M:%S %Z%z").date()
            weekday = ask_time.isoweekday()
        else:
            weekday = datetime.today().isoweekday()

        domain = [('weekday', '=', str(weekday))]
        if doctor:
            domain += [('doctor', '=', int(doctor))]
        slot_ids = sorted(self.search(domain), reverse=True)
        data_dict = {}
        for lt in slot_ids:
            doctor = lt.doctor
            start_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.start_hour * 60, 60))
            end_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.end_hour * 60, 60))
            if doctor.id not in data_dict and doctor.active:
                data_dict[doctor.id] = {
                    'id': doctor.id,
                    'name': doctor.res_partner_medical_doctor_id.name,
                    'count': 1,
                    'time_slots': [{'start_hour': start_hour, 'end_hour': end_hour}]
                }
            elif doctor.id in data_dict:
                data_dict[doctor.id].get('time_slots').append({'start_hour': start_hour, 'end_hour': end_hour})
                count = data_dict[doctor.id].get('count')
                data_dict[doctor.id].update({'count':count+1})

        final_list = []
        for i in data_dict:
            final_list.append(data_dict.get(i))
        return final_list