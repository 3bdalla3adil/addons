from odoo import models, fields, api, _

from datetime import datetime
from odoo.exceptions import UserError


# DONE
class MedicalClinic(models.Model):
    _name = "medical.clinic"
    _description = "Information about the clinic"

    # @api.depends('name')
    # def name_get(self):
    #     result = []
    #     for partner in self:
    #         name = partner.name.name
    #         result.append((partner.id, name))
    #     return result

    name = fields.Char(related='res_partner_medical_clinic_id.name', )
    res_partner_medical_clinic_id = fields.Many2one('res.partner', 'Clinic', required=True, #To Fix Clinic Name field
                                                    # domain=[('is_clinic', '=', "1"), ('is_person', '=', "1")],
                                                    help="Clinic's Name, from the partner list")
    institution = fields.Many2one('res.partner', 'Institution', domain=[('is_institution', '=', "1")],
                                  help="Institution where she/he works")
    code = fields.Char('ID', size=128, help="MD License ID")
    speciality = fields.Many2one('medical.speciality', 'Specialty', required=True, help="Specialty Code")
    equipment_ids = fields.One2many('medical.equipment', 'clinic', string='Equipments', )
    doctor_ids = fields.One2many('medical.doctor', 'clinic_id', string='Assigned Doctors/Nurses', )
    doctor_id = fields.Many2one('medical.doctor', string='Assigned Doctor/Nurse', )  # Assigned Doctor
    info = fields.Text('Extra info')
    user_id = fields.Many2one('res.users', related='res_partner_medical_clinic_id.user_id', string='Clinic User',
                              store=True)
    slot_ids = fields.One2many('clinic.slot', 'clinic_id', 'Availabilities', copy=True)
    active = fields.Boolean('Archive', default=True)
    active_code = fields.Char('ID', default='Test', compute='clinic_active', store=True)

    @api.depends('active_code', 'active')
    def clinic_active(self):
        for record in self:
            if record.active_code:
                if record.active_code and record.active == False:
                    clinic_id = self.env['medical.appointment'].sudo().search(
                        [('clinic.name', '=', record.name), ('active', '=', True)])
                    for doc in clinic_id:
                        doc.write({'active': False})
                if record.active_code and record.active == True:
                    clinic_id = self.env['medical.appointment'].sudo().search(
                        [('clinic.name', '=', record.name), ('active', '=', False)])
                    for doc in clinic_id:
                        doc.write({'active': True})


# DONE
class ClinicSlot(models.Model):
    _name = 'clinic.slot'
    _description = 'Clinic Slot'

    clinic_id = fields.Many2one('medical.clinic', string='Clinic')
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
    def get_clinics_slot(self, target_date=False, clinic=False):
        if target_date:
            ask_time = datetime.strptime(target_date, "%a %b %d %Y %H:%M:%S %Z%z").date()
            weekday = ask_time.isoweekday()
        else:
            weekday = datetime.today().isoweekday()

        domain = [('weekday', '=', str(weekday))]
        if clinic:
            domain += [('clinic_id', '=', int(clinic))]
        slot_ids = sorted(self.search(domain), reverse=True)
        data_dict = {}
        for lt in slot_ids:
            clinic_id = lt.clinic_id
            start_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.start_hour * 60, 60))
            end_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.end_hour * 60, 60))
            if clinic_id.id not in data_dict and clinic_id.active:
                data_dict[clinic_id.id] = {
                    'id': clinic_id.id,
                    'name': clinic_id.res_partner_medical_clinic_id.name,
                    'count': 1,
                    'time_slots': [{'start_hour': start_hour, 'end_hour': end_hour}]
                }
            elif clinic_id.id in data_dict:
                data_dict[clinic_id.id].get('time_slots').append({'start_hour': start_hour, 'end_hour': end_hour})
                count = data_dict[clinic_id.id].get('count')
                data_dict[clinic_id.id].update({'count': count + 1})

        final_list = []
        for i in data_dict:
            final_list.append(data_dict.get(i))
        return final_list

    @api.model
    def get_clinics_slot_validation(self, target_date=False, clinic=False):
        is_available_slot = False
        if target_date:
            ask_time = datetime.strptime(target_date, "%a %b %d %Y %H:%M:%S %Z%z").date()
            weekday = ask_time.isoweekday()
        else:
            weekday = datetime.today().isoweekday()
        domain = [('weekday', '=', str(weekday))]
        if clinic:
            domain += [('clinic_id', '=', int(clinic))]
        slot_ids = sorted(self.search(domain), reverse=True)
        for lt in slot_ids:
            start_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.start_hour * 60, 60))
            end_hour = '{0:02.0f}:{1:02.0f}'.format(*divmod(lt.end_hour * 60, 60))
            ask_time = datetime.strptime(target_date, "%a %b %d %Y %H:%M:%S %Z%z").date()

            start_time = datetime.strptime(start_hour, '%H:%M').time()
            start_date_time = datetime.combine(ask_time, start_time)

            end_time = datetime.strptime(str(end_hour), '%H:%M').time()
            end_date_time = datetime.combine(ask_time, end_time)

            if self.env.context.get('dateToString') and self.env.context.get('from_time'):
                str_date = datetime.strptime(self.env.context.get('dateToString'), "%a %b %d %Y %H:%M:%S %Z%z").date()
                str_date = str(str_date) + ' ' + self.env.context.get('from_time')
                datetime_object = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
                if datetime_object >= start_date_time and datetime_object <= end_date_time:
                    is_available_slot = True
        return is_available_slot
