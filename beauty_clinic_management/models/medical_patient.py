from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

import datetime
# from mock import DEFAULT
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

# PATIENT GENERAL INFORMATION

class MedicalPatient(models.Model):

    def _compute_partner(self):
        pass

    @api.depends('partner_id', 'patient_id')
    def name_get(self):
        result = []
        for record in self:
            name = record.partner_id.name
            if record.patient_id and record.mobile:
                name = '[' + record.mobile + ']' + name
            elif record.partner_id:
                name = '[' + record.partner_id.mobile + ']' + name
                # super(MedicalPatient, self).create(vals)
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(['|','|', '|', '|', '|', '|', ('partner_id', operator, name), ('patient_id', operator, name),
                                ('qid', operator, name),('mobile', operator, name), ('other_mobile', operator, name),
                                ('lastname', operator, name), ('middle_name', operator, name)
                                ])
        if not recs:
            recs = self.search([('partner_id', operator, name)])
        return recs.name_get()

    @api.onchange('dob')
    def onchange_dob(self):
        c_date = datetime.today().strftime('%Y-%m-%d')
        if self.dob:
            if not (str(self.dob) <= c_date):
                raise UserError(_('Birthdate cannot be After Current Date.'))
        return {}

    # @api.onchange('mobile')
    # def onchange_mobile(self):
    #     if self.mobile:
    #         patients = self.env['medical.patient'].search([('mobile', '=', self.mobile)])
    #         if patients:
    #             raise UserError(_('Birthdate cannot be After Current Date.'))
    #     return {}

    # Automatically assign the family code

    @api.onchange('partner_id')
    def onchange_partnerid(self):
        family_code_id = ""
        if self.partner_id:
            self._cr.execute('select family_id from family_members_rel where members_id=%s limit 1',
                             (self.partner_id.id,))
            a = self._cr.fetchone()
            if a:
                family_code_id = a[0]
            else:
                family_code_id = ''
        self.family_code = family_code_id

    # Get the patient age in the following format : "YEARS MONTHS DAYS"
    # It will calculate the age of the patient while the patient is alive. When the patient dies, it will show the age at time of death.

    def _patient_age(self):
        def compute_age_from_dates(patient_dob, patient_deceased, patient_dod):
            now = datetime.now()
            if (patient_dob):
                dob = datetime.strptime(str(patient_dob), '%Y-%m-%d')
                if patient_deceased:
                    dod = datetime.strptime(str(patient_dod), '%Y-%m-%d %H:%M:%S')
                    delta = relativedelta(dod, dob)
                    deceased = " (deceased)"
                else:
                    delta = relativedelta(now, dob)
                    deceased = ''
                years_months_days = str(delta.years) + "y " + str(delta.months) + "m " + str(
                    delta.days) + "d" + deceased
            else:
                years_months_days = "No DoB !"

            return years_months_days

        for rec in self:
            rec.age = compute_age_from_dates(rec.dob, rec.deceased, rec.dod)

    @api.depends_context('critical_info_fun')
    def _medical_alert(self):
        for patient_data in self:
            medical_alert = ''

            if patient_data.medicine_yes:
                medical_alert += patient_data.medicine_yes + '\n'
            if patient_data.card_yes:
                medical_alert += patient_data.card_yes + '\n'
            if patient_data.allergies_yes:
                medical_alert += patient_data.allergies_yes + '\n'
            if patient_data.attacks_yes:
                medical_alert += patient_data.attacks_yes + '\n'
            if patient_data.heart_yes:
                medical_alert += patient_data.heart_yes + '\n'
            if patient_data.bleeding_yes:
                medical_alert += patient_data.bleeding_yes + '\n'
            if patient_data.infectious_yes:
                medical_alert += patient_data.infectious_yes + '\n'
            if patient_data.reaction_yes:
                medical_alert += patient_data.reaction_yes + '\n'
            if patient_data.surgery_yes:
                medical_alert += patient_data.surgery_yes + '\n'
            if patient_data.pregnant_yes:
                medical_alert += patient_data.pregnant_yes + '\n'
            patient_data.critical_info_fun = medical_alert
            if not patient_data.critical_info:
                patient_data.critical_info = medical_alert

    _name = "medical.patient"
    _description = "Patient related information"
    _rec_name = "partner_id"

    name = fields.Char(related='partner_id.name', string='Name', help="Patient Name")
    partner_id = fields.Many2one('res.partner', 'Patient',
                                 domain=[('is_patient', '=', True), ('is_person', '=', True)], help="Patient Name")
    patient_id = fields.Char('Patient ID', size=64,
                             help="Patient Identifier provided by the Health Center. Is not the patient id from the partner form",
                             default=lambda self: _('New'))
    ssn = fields.Char('SSN', size=128, help="Patient Unique Identification Number")
    lastname = fields.Char(related='partner_id.lastname', string='Lastname')
    middle_name = fields.Char(related='partner_id.middle_name', string='Middle Name')
    family_code = fields.Many2one('medical.family_code', 'Family', help="Family Code")
    identifier = fields.Char(string='SSN', related='partner_id.ref', help="Social Security Number or National ID")
    current_insurance = fields.Many2one('medical.insurance', "Insurance",
                                        help="Insurance information. You may choose from the different insurances belonging to the patient")
    sec_insurance = fields.Many2one('medical.insurance', "Insurance", domain="[('partner_id','=',partner_id)]",
                                    help="Insurance information. You may choose from the different insurances belonging to the patient")
    dob = fields.Date('Date of Birth')
    age = fields.Char(compute='_patient_age', string='Patient Age',
                      help="It shows the age of the patient in years(y), months(m) and days(d).\nIf the patient has died, the age shown is the age at time of death, the age corresponding to the date on the death certificate. It will show also \"deceased\" on the field")
    sex = fields.Selection([('m', 'Male'), ('f', 'Female'), ], 'Sex', )
    marital_status = fields.Selection(
        [('s', 'Single'), ('m', 'Married'), ('w', 'Widowed'), ('d', 'Divorced'), ('x', 'Separated'), ],
        'Marital Status')
    blood_type = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O'), ], 'Blood Type')
    rh = fields.Selection([('+', '+'), ('-', '-'), ], 'Rh')
    user_id = fields.Many2one('res.users', related='partner_id.user_id', string='Doctor',
                              help="doctor that logs in the local Medical system (HIS), on the health center. It doesn't necesarily has do be the same as the Primary Care doctor",
                              store=True)
    # medications = fields.One2many('medical.patient.medication', 'name', 'Medications')
    # prescriptions = fields.One2many('medical.prescription.order', 'name', "Prescriptions")
    # diseases_ids = fields.One2many('medical.patient.disease', 'name', 'Diseases')
    critical_info = fields.Text(compute='_medical_alert', string='Medical Alert',
                                help="Write any important information on the patient's disease, surgeries, allergies, ...")
    medical_history = fields.Text('Medical History')
    critical_info_fun = fields.Text(compute='_medical_alert', string='Medical Alert',
                                    help="Write any important information on the patient's disease, surgeries, allergies, ...")
    medical_history_fun = fields.Text('Medical History')
    general_info = fields.Text('General Information', help="General information about the patient")
    deceased = fields.Boolean('Deceased', help="Mark if the patient has died")
    dod = fields.Datetime('Date of Death')
    apt_id = fields.Many2many('medical.appointment', 'pat_apt_rel', 'patient', 'apid', 'Appointments')
    attachment_ids = fields.One2many('ir.attachment', 'patient_id', 'attachments')
    # photo = fields.Binary(related='partner_id.image_1024', string='photos', store=True, readonly=False)
    photo = fields.Binary(related='partner_id.image_1920', string='photos', store=True, readonly=False)
    report_date = fields.Date("Report Date:", default=fields.Datetime.to_string(fields.Datetime.now()))
    occupation_id = fields.Many2one('medical.occupation', 'Occupation')
    primary_doctor_id = fields.Many2one('medical.doctor', 'Primary doctor', )
    referring_doctor_id = fields.Many2one('medical.doctor', 'Referring  doctor', )
    note = fields.Text('Notes', help="Notes and To-Do")
    mobile = fields.Char('Mobile')
    other_mobile = fields.Char('Other Mobile')
    # teeth_treatment_ids = fields.One2many('medical.teeth.treatment', 'patient_id', 'Operations', readonly=True)
    # treatment_ids = fields.One2many('medical.treatment', 'patient_id', 'Operations', readonly=True)
    treatment_ids = fields.One2many('medical.treatment', 'patient_id', 'Operations',)# changed from readonly
    nationality_id = fields.Many2one('patient.nationality', 'Nationality')
    # patient_complaint_ids = fields.One2many('patient.complaint', 'patient_id')
    receiving_treatment = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                           '1. Are you currently receiving treatment from a doctor hospital or clinic ?')
    receiving_medicine = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                          '2. Are you currently taking any prescribed medicines(tablets, inhalers, contraceptive or hormone) ?')
    medicine_yes = fields.Char('Note')
    have_card = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ], '3. Are you carrying a medical warning card ?')
    card_yes = fields.Char('Note')
    have_allergies = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                      '4. Do you suffer from any allergies to any medicines (penicillin) or substances (rubber / latex or food) ?')
    allergies_yes = fields.Char('Note')
    have_feaver = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ], '5. Do you suffer from hay fever or eczema ?')
    have_ashtham = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                    '6. Do you suffer from bronchitis, asthma or other chest conditions ?')
    have_attacks = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                    '7. Do you suffer from fainting attacks, giddlness, blackouts or epllepsy ?')
    attacks_yes = fields.Char('Note')
    have_heart = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                  '8. Do you suffer from heart problems, angina, blood pressure problems, or stroke ?')
    heart_yes = fields.Char('Note')
    have_diabetic = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                     '9. Are you diabetic(or is anyone in your family) ?')
    have_arthritis = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ], '10. Do you suffer from arthritis ?')
    have_bleeding = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                     '11. Do you suffer from bruising or persistent bleeding following injury, tooth extraction or surgery ?')
    bleeding_yes = fields.Char('Note')
    have_infectious = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                       '12. Do you suffer from any infectious disease (including HIV and Hepatitis) ?')
    infectious_yes = fields.Char('Note')
    have_rheumatic = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                      '13. Have you ever had rheumatic fever or chorea ?')
    have_liver = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                  '14. Have you ever had liver disease (e.g jundice, hepatitis) or kidney disease ?')
    have_serious = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                    '15. Have you ever had any other serious illness ?')
    have_reaction = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                     '16. Have you ever had a bad reaction to general or local anaesthetic ?')
    reaction_yes = fields.Char('Note')
    have_surgery = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ], '17. Have you ever had heart surgery ?')
    surgery_yes = fields.Char('Note')
    have_tabacco = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                    '18. Do you smoke any tabacco products now (or in the past ) ?')
    have_gutkha = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                   '19. Do you chew tabacco, pan, use gutkha or supari now (or in the past) ?')
    have_medicine = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ],
                                     '20. Is there any other information which your dentist might need to know about, such as self-prescribe medicine (eg. aspirin) ?')
    have_pregnant = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ], '21. Are you currently pregnant ?')
    pregnant_yes = fields.Char('Note')
    have_breastfeeding = fields.Selection([('YES', 'YES'), ('NO', 'NO'), ], '22. Are you currently breastfeeding ?')
    updated_date = fields.Date('Updated Date')
    arebic = fields.Boolean('Arabic')
    invoice_count = fields.Integer(compute='compute_count')
    active = fields.Boolean(default="True")
    block_reason = fields.Text('Reason')
    qid = fields.Char('QId')
    family_link = fields.Boolean('Family Link')# is linked with family member
    link_partner_id = fields.Many2one('medical.patient', 'Link Partner')# another patient maybe with same number

    def blockpatient(self):
        self.active = False
        return {
            'name': _('Block'),
            'view_mode': 'form',
            'res_model': 'block.reason',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_id': self.env.ref('beauty_clinic_management.block_reason_wizard').id,
            'context': {'default_patient_id': self.id},
        }

    def unblockpatient(self):
        self.active = True

    def get_user_name(self):
        get_doctor_id = self.env['medical.appointment'].search([('patient', '=', self.id)], limit=1)
        return get_doctor_id.doctor.name

    def compute_count(self):
        for record in self:
            record.invoice_count = self.env['account.move'].search_count(
                [('partner_id', '=', record.partner_id.id), ('move_type', '!=', 'entry')])

    _sql_constraints = [
        ('name_uniq', 'unique (partner_id)', 'The Patient already exists'),
        ('patient_id_uniq', 'CHECK(1=1)', 'The Patient ID already exists'),
        # ('patient_id_uniq', 'unique (patient_id)', 'The Patient ID already exists'),
        ('qid_uniq', 'unique (qid)', 'The Patient already exists'),
        #('mobile_number_uniq', 'CHECK(1=1)', 'This Mobile Number already exists'),
    ]

    def get_invoices(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('partner_id', '=', self.partner_id.id), ('move_type', '!=', 'entry')],
            'context': "{'create': False}"
        }

    def get_img(self):
        for rec in self:
            res = {}
            img_lst_ids = []
            imd = self.env['ir.model.data']
            action_view_id = imd.xmlid_to_res_id('action_result_image_view')
            for i in rec.attachment_ids:
                img_lst_ids.append(i.id)
            res['image'] = img_lst_ids
            return {
                'type': 'ir.actions.client',
                'name': 'Result Images',
                'tag': 'result_images',
                'params': {
                    'patient_id': rec.id or False,
                    'model': 'medical.patient',
                    'values': res
                },
            }

    def get_patient_history(self, appt_id):
        return_list = [];
        extra_history = 0;
        total_operation = [];
        return_list.append([])
        if appt_id:
            appt_id_brw = self.env['medical.appointment'].browse(appt_id)
            total_operation = appt_id_brw.operations
            extra_history = len(total_operation)
            for each_patient_operation in self.teeth_treatment_ids:
                if each_patient_operation.description.action_perform == "missing" and each_patient_operation.appt_id.id < appt_id:
                    total_operation += each_patient_operation
        else:
            total_operation = self.teeth_treatment_ids
            extra_history = len(total_operation)
        history_count = 0
        for each_operation in total_operation:
            history_count += 1
            current_tooth_id = each_operation.teeth_id.internal_id
            if each_operation.description:
                desc_brw = self.env['product.product'].browse(each_operation.description.id)
                if desc_brw.action_perform == 'missing':
                    return_list[0].append(current_tooth_id)
                self._cr.execute('select teeth from teeth_code_medical_teeth_treatment_rel where operation = %s' % (
                    each_operation.id,))
                multiple_teeth = self._cr.fetchall()
                multiple_teeth_list = [multiple_teeth_each[0] for multiple_teeth_each in multiple_teeth]
                total_multiple_teeth_list = []
                for each_multiple_teeth_list in multiple_teeth_list:
                    each_multiple_teeth_list_brw = self.env['teeth.code'].browse(each_multiple_teeth_list)
                    total_multiple_teeth_list.append(each_multiple_teeth_list_brw.internal_id)
                    multiple_teeth_list = total_multiple_teeth_list
                other_history = 0
                if history_count > extra_history:
                    other_history = 1
                return_list.append({'other_history': other_history, 'created_date': each_operation.create_date,
                                    'status': each_operation.state, 'multiple_teeth': multiple_teeth_list,
                                    'tooth_id': current_tooth_id, 'surface': each_operation.detail_description,
                                    'desc': {'name': each_operation.description.name,
                                             'id': each_operation.description.id,
                                             'action': each_operation.description.action_perform}})
        return return_list

    def create_lines(self, treatment_lines, patient_id, appt_id):
        # create objects
        medical_teeth_treatment_obj = self.env['medical.teeth.treatment']
        medical_doctor_obj = self.env['medical.doctor']
        product_obj = self.env['product.product']
        teeth_code_obj = self.env['teeth.code']
        # delete previous records
        patient = int(patient_id)
        patient_brw = self.env['medical.patient'].browse(patient)
        partner_brw = patient_brw.partner_id
        if appt_id:
            prev_appt_operations = medical_teeth_treatment_obj.search(
                [('appt_id', '=', int(appt_id)), ('state', '!=', 'completed')])
            prev_appt_operations.unlink()
        else:
            prev_pat_operations = medical_teeth_treatment_obj.search(
                [('patient_id', '=', int(patient_id)), ('state', '!=', 'completed')])
            prev_pat_operations.unlink()

        prev_pat_missing_operations = medical_teeth_treatment_obj.search(
            [('patient_id', '=', int(patient_id)), ('state', '!=', 'completed')])
        for each_prev_pat_missing_operations in prev_pat_missing_operations:
            if each_prev_pat_missing_operations.description.action_perform == 'missing':
                each_prev_pat_missing_operations.unlink()
        if treatment_lines:
            current_doctor = 0;
            for each in treatment_lines:
                if each.get('prev_record') == 'false':
                    all_treatment = each.get('values')
                    if all_treatment:
                        for each_trt in all_treatment:

                            vals = {}
                            category_id = int(each_trt.get('categ_id'))
                            vals['description'] = category_id
                            if 1:
                                if str(each.get('teeth_id')) != 'all':
                                    actual_teeth_id = teeth_code_obj.search(
                                        [('internal_id', '=', int(each.get('teeth_id')))])
                                    vals['teeth_id'] = actual_teeth_id[0].id
                                vals['patient_id'] = patient
                                desc = ''
                                for each_val in each_trt['values']:
                                    if each_val:
                                        desc += each_val + ' '
                                vals['detail_description'] = desc.rstrip()
                                dentist = each.get('dentist')
                                if dentist:
                                    doctor = medical_doctor_obj.search([('name', '=', dentist)])
                                    if doctor:
                                        dentist = doctor.id
                                        vals['dentist'] = dentist
                                        current_doctor = 1
                                status = ''
                                if each.get('status_name') and each.get('status_name') != 'false':
                                    status_name = each.get('status_name')
                                    status = (str(each.get('status_name')))
                                    if status_name == 'in_progress':
                                        status = 'in_progress'
                                    elif status_name == 'planned':
                                        status = 'planned'
                                else:
                                    status = 'planned'
                                vals['state'] = status
                                p_brw = product_obj.browse(vals['description'])
                                vals['amount'] = p_brw.lst_price
                                if appt_id:
                                    vals['appt_id'] = appt_id
                                treatment_id = medical_teeth_treatment_obj.create(vals);
                                if each.get('multiple_teeth'):
                                    full_mouth = each.get('multiple_teeth');
                                    full_mouth = full_mouth.split('_')
                                    operate_on_tooth = []
                                    for each_teeth_from_full_mouth in full_mouth:
                                        actual_teeth_id = teeth_code_obj.search(
                                            [('internal_id', '=', int(each_teeth_from_full_mouth))])
                                        operate_on_tooth.append(actual_teeth_id.id)
                                    treatment_id.write({'teeth_code_rel': [(6, 0, operate_on_tooth)]})

            #                                         cr.execute('insert into teeth_code_medical_teeth_treatment_rel(operation,teeth) values(%s,%s)' % (treatment_id,each_teeth_from_full_mouth))
            invoice_vals = {}
            invoice_line_vals = []
            # Creating invoice lines
            # get account id for products
            jr_search = self.env['account.journal'].search([('type', '=', 'sale')])
            jr_brw = jr_search
            for each in treatment_lines:
                if each.get('prev_record') == 'false':
                    if str(each.get('status_name')).lower() == 'completed':
                        for each_val in each['values']:
                            each_line = [0, False]
                            product_dict = {'product_id': int(each_val['categ_id'])}
                            p_brw = product_obj.browse(int(each_val['categ_id']))
                            if p_brw.action_perform != 'missing':
                                desc = ''
                                features = ''
                                for each_v in each_val['values']:
                                    if each_v:
                                        desc = str(each_v)
                                        features += desc + ' '
                                if each['teeth_id'] != 'all':
                                    actual_teeth_id = teeth_code_obj.search(
                                        [('internal_id', '=', int(each.get('teeth_id')))])
                                    invoice_name = actual_teeth_id.name_get()
                                    product_dict['name'] = str(invoice_name[0][1]) + ' ' + features
                                else:
                                    product_dict['name'] = 'Full Mouth'
                                product_dict['quantity'] = 1
                                product_dict['price_unit'] = p_brw.lst_price
                                acc_obj = self.env['account.account'].search(
                                    [('name', '=', 'Local Sales'), ('user_type_id', '=', 'Income')], limit=1)
                                for account_id in jr_brw:
                                    product_dict[
                                        'account_id'] = account_id.payment_debit_account_id.id if account_id.payment_debit_account_id else acc_obj.id
                                each_line.append(product_dict)
                                invoice_line_vals.append(each_line)
                            # Creating invoice dictionary
                            # invoice_vals['account_id'] = partner_brw.property_account_receivable_id.id
                            if patient_brw.current_insurance:
                                invoice_vals['partner_id'] = patient_brw.current_insurance.company_id.id
                            else:
                                invoice_vals['partner_id'] = partner_brw.id
                            invoice_vals['patient_id'] = partner_brw.id
                            # invoice_vals['partner_id'] = partner_brw.id
                            if current_doctor:
                                invoice_vals['dentist'] = doctor[0].id
                            invoice_vals['move_type'] = 'out_invoice'
                            invoice_vals['insurance_company'] = patient_brw.current_insurance.company_id.id
                            invoice_vals['invoice_line_ids'] = invoice_line_vals

            # creating account invoice
            if invoice_vals:
                self.env['account.move'].create(invoice_vals)
        else:
            return False

    def get_back_address(self, active_patient):
        active_patient = str(active_patient)
        action_rec = self.env['ir.actions.act_window'].search([('res_model', '=', 'medical.patient')])
        action_id = str(action_rec.id)
        address = '/web#id=' + active_patient + '&view_type=form&model=medical.patient&action=' + action_id
        return address

    def get_date(self, date1, lang):
        new_date = ''
        if date1:
            search_id = self.env['res.lang'].search([('code', '=', lang)])
            new_date = datetime.strftime(datetime.strptime(date1, '%Y-%m-%d %H:%M:%S').date(), search_id.date_format)
        return new_date

    def write(self, vals):
        if 'critical_info' in list(vals.keys()):
            #         if 'critical_info' in vals.keys():
            vals['critical_info_fun'] = vals['critical_info']
        #         elif 'critical_info_fun' in vals.keys():
        elif 'critical_info_fun' in list(vals.keys()):
            vals['critical_info'] = vals['critical_info_fun']
        #         if 'medical_history' in vals.keys():
        if 'medical_history' in list(vals.keys()):
            vals['medical_history_fun'] = vals['medical_history']
        #         elif 'medical_history_fun' in vals.keys():
        elif 'medical_history_fun' in list(vals.keys()):
            vals['medical_history'] = vals['medical_history_fun']
        res = super(MedicalPatient, self).write(vals)
        if vals.get('mobile'):
            list_id = [self.id]
            if self.link_partner_id:
                if self.link_partner_id.mobile == vals.get('mobile'):
                    pass
                else:
                    list_id.append(self.link_partner_id.id)
                    patients = self.env["medical.patient"].search(
                        [('mobile', '=', vals.get('mobile')), ('id', 'not in', list_id)])
                    if patients:
                        raise ValidationError(_('This Mobile Number already exists.'))
            else:
                patients = self.env["medical.patient"].search(
                    [('mobile', '=', vals.get('mobile')), ('id', 'not in', list_id)])
                if patients:
                    raise ValidationError(_('This Mobile Number already exists.'))
        return res

    @api.model
    def name_create(self, name):
        # if self.partner_id:
        name1 = mobile = qid = ''
        parts = name.split(',')
        if len(parts) == 3:
            name1, mobile, qid = parts
        elif len(parts) == 2:
            name1, mobile = parts
        elif len(parts) == 1:
            name1 = parts
        else:
            raise UserError('Try again!')

        # Create a new patient if not found
        new_partner = self.env['res.partner'].create({
            'name': name,
            'mobile': mobile,
            'is_patient': True,
            'is_person': True,
        })

        #patient_id = new_partner.id
        self.partner_id = new_partner.id
        self.mobile = mobile
        self.qid = qid
        name = new_partner.id
        res = super(MedicalPatient,self).name_create(name)
        return res

    @api.model
    def create(self, vals):
        if vals.get('critical_info'):
            vals['critical_info_fun'] = vals['critical_info']
        elif vals.get('critical_info_fun'):
            vals['critical_info'] = vals['critical_info_fun']
        if vals.get('medical_history'):
            vals['medical_history_fun'] = vals['medical_history']
        elif vals.get('medical_history_fun'):
            vals['medical_history'] = vals['medical_history_fun']
        c_date = datetime.today().strftime('%Y-%m-%d')
        result = False
        # if vals.get('patient_id', 'New') == 'New':
        #     vals['patient_id'] = self.env['ir.sequence'].next_by_code('medical.patient') or 'New'
        if 'dob' in vals and vals.get('dob'):
            if (vals['dob'] > c_date):
                raise ValidationError(_('Birthdate cannot be After Current Date.'))

        result = super(MedicalPatient, self).create(vals)
        if vals.get('mobile'):
            list_id = [result.id]
            if result.link_partner_id:
                if result.link_partner_id.mobile == vals.get('mobile'):
                    pass
                else:
                    list_id.append(result.link_partner_id.id)
                    patients = self.env["medical.patient"].search(
                        [('mobile', '=', vals.get('mobile')), ('id', 'not in', list_id)])
                    if patients:
                        raise ValidationError(_('This Mobile Number already exists.'))
            else:
                patients = self.env["medical.patient"].search(
                    [('mobile', '=', vals.get('mobile')), ('id', 'not in', list_id)])
                if patients:
                    raise ValidationError(_('This Mobile Number already exists.'))


        if vals.get('patient_id', 'New') == 'New':
            seq_date = datetime.now().strftime('%Y')
            seq = self.env['ir.sequence'].next_by_code('medical.patient') or 'New'
            result.patient_id = f'{seq_date}/{seq}'

        return result

    #
    #     def get_img(self):
    #         for rec in self:
    #             res = {}
    #             img_lst_ids = []
    #             imd = self.env['ir.model.data']
    #             action_view_id = imd.xmlid_to_res_id('action_result_image_view')
    #             for i in rec.attachment_ids:
    #                 img_lst_ids.append(i.id)
    #             res['image'] = img_lst_ids
    #
    #             return {
    #             'type': 'ir.actions.client',
    #             'name': 'Patient image',
    #             'tag': 'result_images',
    #             'params': {
    #                'patient_id':  rec.id  or False,
    #                'model':  'medical.patient',
    #                'values': res
    #             },
    #         }

    def open_chart(self):
        for rec in self:
            appt_id = self.env['medical.appointment'].search([
                ('state', 'not in', ['done', 'cancel']),
                ('patient', '=', self.id),
            ], order='id DESC', limit=1)
            if not appt_id:
                raise UserError(
                    _('Currently no running any appointment for %s!\n Please create the appointment for %s') % (
                    self.partner_id.name, self.partner_id.name))
            appt_id = appt_id.id
            context = dict(self._context or {})

            #             if 'appointment_id_new' in context.keys():
            if 'appointment_id_new' in list(context.keys()):
                appt_id = context['appointment_id_new']
            if context is None:
                context = {}
            imd = self.env['ir.model.data']
            action_view_id = self.env['ir.model.data']._xmlid_to_res_id('action_open_human_body_chart')
            # action_view_id = imd.xmlid_to_res_id('action_open_human_body_chart')
            teeth_obj = self.env['chart.selection'].search([])
            # teeth = teeth_obj[-1]
            res_open_chart = {
                'type': 'ir.actions.client',
                'name': 'Human Body Chart',
                'tag': 'human_body_chart',
                'params': {
                    'patient_id': rec.id or False,
                    'appt_id': appt_id,
                    'model': 'medical.patient',
                    # 'type': teeth.type,
                    'dentist': rec.referring_doctor_id.id
                },
            }
            return res_open_chart

    def close_chart(self):
        res_close_chart = {'type': 'ir.actions.client', 'tag': 'history_back'}
        return res_close_chart

    @api.model
    def _create_birthday_scheduler(self):
        self.create_birthday_scheduler()

    @api.model
    def create_birthday_scheduler(self):
        #         alert_id = self.pool.get('ir.cron').search(cr, uid, [('model', '=', 'medical.patient'), ('function', '=', 'create_birthday_scheduler')])
        #         alert_record = self.pool.get('ir.cron').browse(cr, uid, alert_id[0], context=context)
        #         alert_date = datetime.strptime(alert_record.nextcall, "%Y-%m-%d %H:%M:%S").date()
        alert_date1 = datetime.today().strftime('%Y-%m-%d')
        alert_date = datetime.strptime(str(alert_date1), "%Y-%m-%d")
        patient_ids = self.search([])
        for each_id in patient_ids:
            birthday_alert_id = self.env['patient.birthday.alert'].search([('patient_id', '=', each_id.id)])
            if not birthday_alert_id:
                if each_id.dob:
                    dob = datetime.strptime(str(each_id.dob), "%Y-%m-%d")
                    if dob.day <= alert_date.day or dob.month <= alert_date.month or dob.year <= alert_date.year:
                        self.env['patient.birthday.alert'].create({'patient_id': each_id.id,
                                                                   'dob': dob,
                                                                   'date_create': datetime.today().strftime(
                                                                       '%Y-%m-%d')})

        return True

    @api.model
    def _create_planned_visit_scheduler(self):
        self.create_planned_visit_scheduler()

    @api.model
    def create_planned_visit_scheduler(self):
        patient_ids = self.search([])
        patient_dict_sent = []
        patient_dict_not_sent = []
        flag1 = 0
        flag2 = 0
        for each_id in patient_ids:
            for service_id in each_id.teeth_treatment_ids:
                if service_id.state == 'completed':
                    if service_id.description.is_planned_visit:
                        create_date_obj = service_id.create_date
                        if service_id.description.duration == 'three_months':
                            check_date = (datetime.now().date() - timedelta(3 * 365 / 12)).isoformat()
                        elif service_id.description.duration == 'six_months':
                            check_date = (datetime.now().date() - timedelta(6 * 365 / 12)).isoformat()
                        elif service_id.description.duration == 'one_year':
                            check_date = (datetime.now().date() - timedelta(12 * 365 / 12)).isoformat()

                        if str(create_date_obj)[0:10] < check_date:
                            flag1 = 0
                            for each_pat in patient_dict_sent:
                                if each_pat['patient_id'] == each_id.id and each_pat[
                                    'product_id'] == service_id.description.id:
                                    flag1 = 1
                                    if str(service_id.create_date)[0:10] > each_pat['date']:
                                        each_pat['date'] = str(service_id.create_date)[0:10]
                                    break
                            if flag1 == 0:
                                patient_dict_sent.append({'patient_id': each_id.id, 'name': each_id.name.name,
                                                          'product_id': service_id.description.id,
                                                          'pname': service_id.description.name,
                                                          'date': str(service_id.create_date)[0:10]})
                        else:
                            flag2 = 0
                            for each_pat in patient_dict_not_sent:
                                if each_pat['patient_id'] == each_id.id and each_pat[
                                    'product_id'] == service_id.description.id:
                                    flag2 = 1
                                    if str(service_id.create_date)[0:10] > each_pat['date']:
                                        each_pat['date'] = str(service_id.create_date)[0:10]
                                    break

                            if flag2 == 0:
                                patient_dict_not_sent.append({'patient_id': each_id.id, 'name': each_id.partner_id.name,
                                                              'product_id': service_id.description.id,
                                                              'pname': service_id.description.name,
                                                              'date': str(service_id.create_date)[0:10]})
        for each_not_sent in patient_dict_not_sent:
            for each_sent in patient_dict_sent:
                if each_sent['patient_id'] == each_not_sent['patient_id'] and each_sent['product_id'] == each_not_sent[
                    'product_id']:
                    patient_dict_sent.remove(each_sent)
                    break
        palnned_obj = self.env['planned.visit.alert']
        visit_ids = palnned_obj.search([])
        for each in patient_dict_not_sent:
            flag3 = 0
            for each_record in visit_ids:
                if each_record.patient_name.id == each['patient_id'] and each_record.treatment_name.id == each[
                    'product_id']:
                    flag3 = 1
                    break
            if flag3 == 0:
                palnned_obj.create({'patient_name': each['patient_id'],
                                    'treatment_name': each['product_id'], 'operated_date': each['date']})

        return True
