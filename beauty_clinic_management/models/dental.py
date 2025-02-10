# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

import datetime
import hashlib
import logging
# from mock import DEFAULT
from datetime import datetime

_logger = logging.getLogger(__name__)


from odoo import models, fields, api

#DONE - Worked with state_color
class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('missed', 'Missed'),
        ('checkin', 'Check-in'),
        ('ready', 'Ready'),
        ('cancel', 'Cancel'),
        ('done', 'Done')
    ], string="State", default='draft')

    @api.depends('state')
    def _compute_color_index(self):
        state_color_map = {
            'draft': '#FFFFE0',  # LightYellow
            'confirmed': '#FFA500', # Orange
            'missed': '#98FB98',
            'checkin': '#ADD8E6',  # LightBlue
            'ready': '#DDA0DD',
            'cancel': '#FFCCCC',  # LightRed
            'done': '#FFFACD',  # LightGreen
        }
        for event in self:
            # Default to white if state not found
            event.color_index = state_color_map.get(event.state, '#FFFFFF')

    color_index = fields.Char(compute='_compute_color_index', string='Color Index')
# =============================================================================================================
# =============================================================================================================


class MedicalInsurance(models.Model):
    _name = "medical.insurance"
    _description = "Medical Insurance"
    _rec_name = "name"

    @api.depends('number', 'company_id')
    def name_get(self):
        result = []
        for insurance in self:
            name = insurance.company_id.name + ':' + insurance.number
            result.append((insurance.id, name))
        return result

    name = fields.Char(related="res_partner_insurance_id.name")
    res_partner_insurance_id = fields.Many2one('res.partner', 'Owner')
    number = fields.Char('Number', required=True)
    company_id = fields.Many2one('res.partner', 'Insurance Company', domain="[('is_insurance_company', '=', '1')]",
                                 required=True)
    member_since = fields.Date('Member since')
    member_exp = fields.Date('Expiration date')
    category = fields.Char('Category', help="Insurance company plan / category")
    type = fields.Selection([('state', 'State'), ('labour_union', 'Labour Union / Syndical'), ('private', 'Private'), ],
                            'Insurance Type')
    notes = fields.Text('Extra Info')
    plan_id = fields.Many2one('medical.insurance.plan', 'Plan', help='Insurance company plan')

# DONE!
class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Res Partner"

    @api.model
    def send_notification(self, notification):
        res = self.env['bus.bus']._sendone(
            (self._cr.dbname, 'res.partner', self.id),
            'display_notification',
            notification
        )


    date = fields.Date('Partner since', help="Date of activation of the partner or patient")
    alias = fields.Char('alias')
    ref = fields.Char('ID Number')
    is_person = fields.Boolean('Person', help="Check if the partner is a person.")
    is_patient = fields.Boolean('Patient', help="Check if the partner is a patient")
    is_clinic = fields.Boolean('Clinic', help="Check if the partner is a clinic")
    is_doctor = fields.Boolean('Doctor', help="Check if the partner is a doctor")
    is_institution = fields.Boolean('Institution', help="Check if the partner is a Medical Center")
    is_insurance_company = fields.Boolean('Insurance Company', help="Check if the partner is a Insurance Company")
    is_pharmacy = fields.Boolean('Pharmacy', help="Check if the partner is a Pharmacy")
    middle_name = fields.Char('Middle Name',  help="Middle Name")
    lastname = fields.Char('Last Name',  help="Last Name")
    insurance_ids = fields.One2many('medical.insurance', 'name', "Insurance")
    treatment_id = fields.Many2many('product.product', 'treatment_insurance_company_relation', 'treatment_id',
                                    'insurance_company_id', 'Treatment')

    _sql_constraints = [
        ('ref_uniq', 'unique (ref)', 'The partner or patient code must be unique')
    ]

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        active_company = self.env.company
        if view_type == 'form' and active_company.id == 1:
            for node in arch.xpath("//group[@name='unit_info']"):
                node.set('invisible', '1')
            for node in arch.xpath("//group[@name='date_info']"):
                node.set('invisible', '1')
            for node in arch.xpath("//group[@name='invoice_id']"):
                node.set('invisible', '1')
            for node in arch.xpath("//button[@name='action_generate_pdc']"):
                node.set('invisible', '1')

        elif view_type == 'form' and active_company.id != 1:
            for node in arch.xpath("//page[@name='insurance_ids']"):
                node.set('invisible', '1')
            for node in arch.xpath("//notebook[@name='treatment_ids']"):
                node.set('invisible', '1')
            for node in arch.xpath("//field[@name='customer_id']"):
                node.set('invisible', '1')
            # for node in arch.xpath("//field[@name='pdc_state']"):
            #     node.set('invisible', '1')
            for node in arch.xpath("//field[@name='cheque_no']"):
                node.set('invisible', '1')
            for node in arch.xpath("//field[@name='mobile']"):
                node.set('invisible', '1')
            for node in arch.xpath("//field[@name='customer_id']"):
                node.set('invisible', '1')
            for node in arch.xpath("//field[@name='pdc_state']"):
                node.set('invisible', '1')

        return arch, view

    @api.depends('name', 'lastname')
    def name_get(self):
        result = []
        for partner in self:
            name = partner.name
            if partner.middle_name:
                name += ' ' + partner.middle_name
            if partner.lastname:
                name = partner.lastname + ', ' + name
            result.append((partner.id, name))
        return result

class ProductProduct(models.Model):
    # _name = "product.product"
    _description = "Product"
    _inherit = "product.product"

    action_perform = fields.Selection([('action', 'Action'), ('missing', 'Missing'), ('composite', 'Composite')],
                                      'Action perform', default='action')
    is_medicament = fields.Boolean('Medicament', help="Check if the product is a medicament")
    is_insurance_plan = fields.Boolean('Insurance Plan', help='Check if the product is an insurance plan')
    is_treatment = fields.Boolean('Treatment', help="Check if the product is a Treatment")
    is_planned_visit = fields.Boolean('Planned Visit')
    is_material = fields.Boolean('Material')
    duration = fields.Selection(
        [('three_months', 'Three Months'), ('six_months', 'Six Months'), ('one_year', 'One Year')], 'Duration((long))')

    duration_id = fields.Many2one('duration.duration', 'Duration')
    #     insurance_company_ids = fields.One2many('res.partner','treatment_id',string="Insurance Company")
    insurance_company_id = fields.Many2many('res.partner', 'treatment_insurance_company_relation',
                                            'insurance_company_id', 'treatment_id', 'Insurance Company')
    clinic = fields.Many2one('medical.clinic',string='Clinic')
    # clinic_ids = fields.Many2many('medical.clinic', 'treatment_clinic_relation',
    clinic_ids = fields.Many2many('medical.clinic', 'service_clinic_relation',
                                            'clinic_id', 'treatment_id', string='Clinics')
    equipment_id = fields.One2many('medical.equipment','clinic',string='Equipment')

    def get_treatment_charge(self):
        return self.lst_price

    # def get_operation_names(self, category):
    #     operations = {}
    #     product_records = self.env['product.product'].search(
    #         [('is_treatment', '=', True), ('categ_id.name', '=', category)])
    #     for each_brw in product_records:
    #         operations[each_brw.name] = {
    #             'id': each_brw.id, 'type': each_brw.part_type}
    #     return operations



class ClaimManagement(models.Model):
    _name = 'dental.insurance.claim.management'
    _description = 'Beauty Insurance Claim Management'

    claim_date = fields.Date(string='Claim Date')
    name = fields.Many2one('medical.patient', string='Patient')
    insurance_company = fields.Many2one('res.partner', string='Insurance Company',
                                        domain="[('is_insurance_company', '=', True)]")
    insurance_policy_card = fields.Char(string='Insurance Policy Card')
    treatment_done = fields.Boolean(string='Treatment Done')

class InsurancePlan(models.Model):
    _name = 'medical.insurance.plan'
    _description = "Medical Insurance Plan"

    # @api.depends('name', 'code')
    # def name_get(self):
    #     result = []
    #     for insurance in self:
    #         name = insurance.code + ' ' + insurance.name.name
    #         result.append((insurance.id, name))
    #     return result

    is_default = fields.Boolean(string='Default Plan',
                                help='Check if this is the default plan when assigning this insurance company to a patient')
    name = fields.Char(related='product_insurance_plan_id.name')
    product_insurance_plan_id = fields.Many2one('product.product', string='Plan', required=True,
                                                domain="[('type', '=', 'service'), ('is_insurance_plan', '=', True)]",
                                                help='Insurance company plan')
    company_id = fields.Many2one('res.partner', string='Insurance Company', required=True,
                                 domain="[('is_insurance_company', '=', '1')]")
    notes = fields.Text('Extra info')
    code = fields.Char( required=True, index=True)


# TEMPLATE USED IN MEDICATION AND PRESCRIPTION ORDERS

class MedicalMedicationTemplate(models.Model):
    _name = "medical.medication.template"
    _description = "Template for medication"

    medicament = fields.Many2one('medical.medicament', 'Medicament', help="Prescribed Medicament", required=True, )
    indication = fields.Many2one('medical.pathology', 'Indication',
                                 help="Choose a disease for this medicament from the disease list. It can be an existing disease of the patient or a prophylactic.")
    dose = fields.Float('Dose', help="Amount of medication (eg, 250 mg ) each time the patient takes it")
    dose_unit = fields.Many2one('medical.dose.unit', 'dose unit', help="Unit of measure for the medication to be taken")
    route = fields.Many2one('medical.drug.route', 'Administration Route',
                            help="HL7 or other standard drug administration route code.")
    form = fields.Many2one('medical.drug.form', 'Form', help="Drug form, such as tablet or gel")
    qty = fields.Integer('x', default=1, help="Quantity of units (eg, 2 capsules) of the medicament")
    common_dosage = fields.Many2one('medical.medication.dosage', 'Frequency',
                                    help="Common / standard dosage frequency for this medicament")
    frequency = fields.Integer('Frequency',
                               help="Time in between doses the patient must wait (ie, for 1 pill each 8 hours, put here 8 and select 'hours' in the unit field")
    frequency_unit = fields.Selection([
        ('seconds', 'seconds'),
        ('minutes', 'minutes'),
        ('hours', 'hours'),
        ('days', 'days'),
        ('weeks', 'weeks'),
        ('wr', 'when required'),
    ], 'unit', index=True, default='hours')
    admin_times = fields.Char('Admin hours',
                              help='Suggested administration hours. For example, at 08:00, 13:00 and 18:00 can be encoded like 08 13 18')
    duration = fields.Integer('Treatment duration',
                              help="Period that the patient must take the medication. in minutes, hours, days, months, years or indefinately")
    duration_period = fields.Selection(
        [('minutes', 'minutes'), ('hours', 'hours'), ('days', 'days'), ('months', 'months'), ('years', 'years'),
         ('indefinite', 'indefinite')], 'Treatment Period', default='days',
        help="Period that the patient must take the medication. in minutes, hours, days, months, years or indefinately")
    start_treatment = fields.Datetime('Start of treatment', default=fields.Datetime.now)
    end_treatment = fields.Datetime('End of treatment')

    _sql_constraints = [
        ('dates_check', "CHECK (start_treatment < end_treatment)",
         "Treatment Star Date must be before Treatment End Date !"),
    ]

class MedicamentCategory(models.Model):
    _description = 'Medicament Categories'
    _name = 'medicament.category'
    _order = 'parent_id,id'

    @api.depends('name', 'parent_id')
    def name_get(self):
        result = []
        for partner in self:
            name = partner.name
            if partner.parent_id:
                name = partner.parent_id.name + ' / ' + name
            result.append((partner.id, name))
        return result

    @api.model
    def _name_get_fnc(self):
        res = self._name_get_fnc()
        return res

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create a recursive category.'))

    name = fields.Char('Category Name', required=True, )
    parent_id = fields.Many2one('medicament.category', 'Parent Category', index=True)
    complete_name = fields.Char(compute='_name_get_fnc', string="Name")
    child_ids = fields.One2many('medicament.category', 'parent_id', 'Children Category')

class MedicalMedicament(models.Model):
    # @api.depends('name')
    # def name_get(self):
    #     result = []
    #     for partner in self:
    #         name = partner.name.name
    #         result.append((partner.id, name))
    #     return result

    _description = 'Medicament'
    _name = "medical.medicament"

    name = fields.Char(related="product_medicament_id.name")
    product_medicament_id = fields.Many2one('product.product', 'Name', required=True,
                                            domain=[('is_medicament', '=', "1")], help="Commercial Name")

    category = fields.Many2one('medicament.category', 'Category')
    active_component = fields.Char('Active component',  help="Active Component")
    therapeutic_action = fields.Char('Therapeutic effect',  help="Therapeutic action")
    composition = fields.Text('Composition', help="Components")
    indications = fields.Text('Indication', help="Indications")
    dosage = fields.Text('Dosage Instructions', help="Dosage / Indications")
    overdosage = fields.Text('Overdosage', help="Overdosage")
    pregnancy_warning = fields.Boolean('Pregnancy Warning',
                                       help="Check when the drug can not be taken during pregnancy or lactancy")
    pregnancy = fields.Text('Pregnancy and Lactancy', help="Warnings for Pregnant Women")
    presentation = fields.Text('Presentation', help="Packaging")
    adverse_reaction = fields.Text('Adverse Reactions')
    storage = fields.Text('Storage Conditions')
    price = fields.Float(related='product_medicament_id.lst_price', string='Price')
    qty_available = fields.Float(related='product_medicament_id.qty_available', string='Quantity Available')
    notes = fields.Text('Extra Info')
    pregnancy_category = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('X', 'X'),
        ('N', 'N'),
    ], 'Pregnancy Category',
        help='** FDA Pregancy Categories ***\n'
             'CATEGORY A :Adequate and well-controlled human studies have failed'
             ' to demonstrate a risk to the fetus in the first trimester of'
             ' pregnancy (and there is no evidence of risk in later'
             ' trimesters).\n\n'
             'CATEGORY B : Animal reproduction studies have failed todemonstrate a'
             ' risk to the fetus and there are no adequate and well-controlled'
             ' studies in pregnant women OR Animal studies have shown an adverse'
             ' effect, but adequate and well-controlled studies in pregnant women'
             ' have failed to demonstrate a risk to the fetus in any'
             ' trimester.\n\n'
             'CATEGORY C : Animal reproduction studies have shown an adverse'
             ' effect on the fetus and there are no adequate and well-controlled'
             ' studies in humans, but potential benefits may warrant use of the'
             ' drug in pregnant women despite potential risks. \n\n '
             'CATEGORY D : There is positive evidence of human fetal  risk based'
             ' on adverse reaction data from investigational or marketing'
             ' experience or studies in humans, but potential benefits may warrant'
             ' use of the drug in pregnant women despite potential risks.\n\n'
             'CATEGORY X : Studies in animals or humans have demonstrated fetal'
             ' abnormalities and/or there is positive evidence of human fetal risk'
             ' based on adverse reaction data from investigational or marketing'
             ' experience, and the risks involved in use of the drug in pregnant'
             ' women clearly outweigh potential benefits.\n\n'
             'CATEGORY N : Not yet classified')

class MedicalSpeciality(models.Model):
    _name = "medical.speciality"
    _description = "Medical Speciality"

    name = fields.Char('Description', required=True, help="ie, Addiction Psychiatry")
    code = fields.Char('Code', help="ie, ADP")

    _sql_constraints = [
        ('code_uniq', 'unique (name)', 'The Medical Specialty code must be unique')]

class MedicalFamilyCode(models.Model):
    _name = "medical.family_code"
    _description = "Medical Family Code"
    # _rec_name = "name"

    name = fields.Char(related="res_partner_family_medical_id.name")
    res_partner_family_medical_id = fields.Many2one('res.partner', 'Name', required=True,
                                                    help="Family code within an operational sector")
    members_ids = fields.Many2many('res.partner', 'family_members_rel', 'family_id', 'members_id', 'Members',
                                   domain=[('is_person', '=', "1")])
    info = fields.Text('Extra Information')

    _sql_constraints = [('code_uniq', 'unique (res_partner_family_medical_id)', 'The Family code name must be unique')]


class MedicalOccupation(models.Model):
    _name = "medical.occupation"
    _description = "Occupation / Job"

    name = fields.Char('Occupation', required=True)
    code = fields.Char('Code')

    _sql_constraints = [
        ('occupation_name_uniq', 'unique(name)', 'The Name must be unique !'),
    ]


class AccountMove(models.Model):
    _inherit = "account.move"
    _description = "Account Move"

    doctor = fields.Many2one('medical.doctor', 'Doctor')
    clinic = fields.Many2one('medical.clinic', 'Clinic')
    patient = fields.Many2one('medical.patient')
    patient_id = fields.Many2one('medical.patient')
    insurance_company = fields.Many2one('res.partner', 'Insurance Company',
                                        domain=[('is_insurance_company', '=', True)])

    @api.onchange('partner_id')
    def partneronchange(self):
        if (self.partner_id and self.partner_id.is_patient):
            patient_id = self.env['medical.patient'].search([('partner_id', '=', self.partner_id.id)])
            self.patient = patient_id.id
        else:
            self.patient = False

class Website(models.Model):
    _inherit = 'website'
    _description = "Website"

    def get_image(self, a):
        #         if 'image' in a.keys():
        if 'image' in list(a.keys()):
            return True
        else:
            return False

    def get_type(self, record1):
        categ_type = record1['type']
        categ_ids = self.env['product.category'].search([('name', '=', categ_type)])
        if categ_ids['type'] == 'view':
            return False
        return True

    def check_next_image(self, main_record, sub_record):
        if len(main_record['image']) > sub_record:
            return 1
        else:
            return 0

    def image_url_new(self, record1):
        """Returns a local url that points to the image field of a given browse record."""
        lst = []
        size = None
        field = 'datas'
        record = self.env['ir.attachment'].browse(self.ids)
        cnt = 0
        for r in record:
            if r.store_fname:
                cnt = cnt + 1
                model = r._name
                sudo_record = r.sudo()
                id = '%s_%s' % (r.id, hashlib.sha1(
                    (str(sudo_record.write_date) or str(sudo_record.create_date) or '').encode('utf-8')).hexdigest()[
                                      0:7])
                if cnt == 1:
                    size = '' if size is None else '/%s' % size
                else:
                    size = '' if size is None else '%s' % size
                lst.append('/website/image/%s/%s/%s%s' % (model, id, field, size))
        return lst


class PatientNationality(models.Model):
    _name = "patient.nationality"
    _description = "Patient Nationality"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code')


# PATIENT MEDICATION TREATMENT
class MedicalPatientMedication(models.Model):
    _name = "medical.patient.medication"
    _inherits = {'medical.medication.template': 'template'}
    _description = "Patient Medication"

    template = fields.Many2one('medical.medication.template', 'Template ID', required=True, index=True,
                               )
    name = fields.Many2one('medical.patient', 'Patient ID', readonly=True)
    doctor = fields.Many2one('medical.doctor', 'Doctor', help="Doctor who prescribed the medicament")
    is_active = fields.Boolean('Active', default=True,
                               help="Check this option if the patient is currently taking the medication")
    discontinued = fields.Boolean('Discontinued')
    course_completed = fields.Boolean('Course Completed')
    discontinued_reason = fields.Char('Reason for discontinuation',
                                      help="Short description for discontinuing the treatment")
    adverse_reaction = fields.Text('Adverse Reactions',
                                   help="Specific side effects or adverse reactions that the patient experienced")
    notes = fields.Text('Extra Info')
    patient_id = fields.Many2one('medical.patient', 'Patient')

    @api.onchange('course_completed', 'discontinued', 'is_active')
    def onchange_medication(self):
        family_code_id = ""
        if self.course_completed:
            self.is_active = False
            self.discontinued = False
        elif self.is_active == False and self.discontinued == False and self.course_completed == False:
            self.is_active = True
        if self.discontinued:
            self.is_active = False
            self.course_completed = False
        elif self.is_active == False and self.discontinued == False and self.course_completed == False:
            self.is_active = True
        if self.is_active:
            self.course_completed = False
            self.discontinued = False
        elif self.is_active == False and self.discontinued == False and self.course_completed == False:
            self.course_completed = True


# PRESCRIPTION ORDER DONE!
class MedicalPrescriptionOrder(models.Model):
    _name = "medical.prescription.order"
    _description = "prescription order"

    @api.model
    def _get_default_clinic(self):
        doc_ids = None
        partner_ids = self.env['res.partner'].search([('user_id', '=', self.env.user.id), ('is_clinic', '=', True)])
        if partner_ids:
            partner_ids = [x.id for x in partner_ids]
            doc_ids = [x.id for x in self.env['medical.clinic'].search([('name', 'in', partner_ids)])]
        return doc_ids

    @api.model
    def _get_default_doctor(self):
        doc_ids = None
        partner_ids = self.env['res.partner'].search([('user_id', '=', self.env.user.id), ('is_doctor', '=', True)])
        if partner_ids:
            partner_ids = [x.id for x in partner_ids]
            doc_ids = [x.id for x in self.env['medical.doctor'].search([('name', 'in', partner_ids)])]
        return doc_ids

    name = fields.Many2one('medical.patient', string="Patient ID", required=True)
    prescription_id = fields.Char('Prescription ID',
                                  help='Type in the ID of this prescription')
    prescription_date = fields.Datetime('Prescription Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', 'Log In User', readonly=True, default=lambda self: self.env.user)
    pharmacy = fields.Many2one('res.partner', 'Pharmacy', domain=[('is_pharmacy', '=', True)])
    prescription_line = fields.One2many('medical.prescription.line', 'name', 'Prescription line')
    notes = fields.Text('Prescription Notes')
    pid1 = fields.Many2one('medical.appointment', 'Appointment', )
    doctor = fields.Many2one('medical.doctor', 'Prescribing Doctor', help="Doctor's Name",default=_get_default_doctor)
    clinic = fields.Many2one('medical.clinic', 'Prescribing Clinic', help="Clinic's Name",
                             default=_get_default_clinic)
    p_name = fields.Char('Demo', default=False)
    no_invoice = fields.Boolean('Invoice exempt')
    invoice_done = fields.Boolean('Invoice Done')
    state = fields.Selection([('tobe', 'To be Invoiced'), ('invoiced', 'Invoiced'), ('cancel', 'Cancel')],
                             'Invoice Status', default='tobe')
    inv_id = fields.Many2one('account.move', 'Invoice', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', required=True)

    _sql_constraints = [
        ('pid1', 'unique (pid1)', 'Prescription must be unique per Appointment'),
        ('prescription_id', 'unique (prescription_id)', 'Prescription ID must be unique')]

    @api.onchange('name')
    def onchange_name(self):
        domain_list = []
        domain = {}
        if self.name:
            apt_ids = self.search([('name', '=', self.name.id)])
            for apt in apt_ids:
                if apt.pid1:
                    domain_list.append(apt.pid1.id)
        domain['pid1'] = [('id', 'not in', domain_list)]
        return {'domain': domain}

    @api.model
    def create(self, vals):
        if vals.get('prescription_id', 'New') == 'New':
            vals['prescription_id'] = self.env['ir.sequence'].next_by_code('medical.prescription') or 'New'
        result = super(MedicalPrescriptionOrder, self).create(vals)
        return result

    #         def onchange_p_name(self, cr, uid, ids, p_name,context = None ):
    #          n_name=context.get('name')
    #          d_name=context.get('clinic_id')
    #          v={}
    #          v['name'] =  n_name
    #          v['clinic'] =  d_name
    #          return {'value': v}

    def get_date(self, date1, lang):
        new_date = ''
        if date1:
            search_id = self.env['res.lang'].search([('code', '=', lang)])
            new_date = datetime.strftime(datetime.strptime(date1, '%Y-%m-%d %H:%M:%S').date(), search_id.date_format)
        return new_date

    def _prepare_invoice(self):
        invoice_vals = {
            'move_type': 'out_invoice',
            'narration': self.notes,
            'invoice_user_id': self.user_id and self.user_id.id,
            'partner_id': self.name.partner_id.id,
            'invoice_line_ids': [],
            'doctor': self.doctor.id,
            'clinic': self.clinic.id,
            'invoice_date': datetime.today()
        }
        return invoice_vals

    def create_invoices(self):
        if not self.prescription_line:
            raise UserError(_("Please add medicine line."))
        invoice_vals = self._prepare_invoice()
        for line in self.prescription_line:
            res = {}
            res.update({
                #                 'name': line.medicine_id.name.name,
                'product_id': line.medicine_id.name.id,
                'price_unit': line.medicine_id.price,
                'quantity': line.quantity,
            })
            invoice_vals['invoice_line_ids'].append((0, 0, res))
        inv_id = self.env['account.move'].create(invoice_vals)
        if inv_id:
            self.inv_id = inv_id.id
            self.state = 'invoiced'
        return inv_id

    @api.onchange('pid1')
    def get_appoinment_details(self):
        if self.pid1:
            self.clinic = self.pid1.clinic
            self.doctor = self.pid1.doctor
            self.name = self.pid1.patient


# PRESCRIPTION LINE
class MedicalPrescriptionLine(models.Model):
    _name = "medical.prescription.line"
    _description = "Basic prescription object"

    medicine_id = fields.Many2one('medical.medicine.prag', 'Medicine', required=True, )
    name = fields.Many2one('medical.prescription.order', 'Prescription ID')
    quantity = fields.Integer('Quantity', default=1)
    note = fields.Char('Note',  help='Short comment on the specific drug')
    dose = fields.Float('Dose', help="Amount of medication (eg, 250 mg ) each time the patient takes it")
    dose_unit = fields.Many2one('medical.dose.unit', 'Dose Unit', help="Unit of measure for the medication to be taken")
    form = fields.Many2one('medical.drug.form', 'Form', help="Drug form, such as tablet or gel")
    qty = fields.Integer('x', default=1, help="Quantity of units (eg, 2 capsules) of the medicament")
    common_dosage = fields.Many2one('medical.medication.dosage', 'Frequency',
                                    help="Common / standard dosage frequency for this medicament")
    duration = fields.Integer('Duration',
                              help="Time in between doses the patient must wait (ie, for 1 pill each 8 hours, put here 8 and select 'hours' in the unit field")
    duration_period = fields.Selection([
        ('seconds', 'seconds'),
        ('minutes', 'minutes'),
        ('hours', 'hours'),
        ('days', 'days'),
        ('weeks', 'weeks'),
        ('wr', 'when required'),
    ], 'Duration Unit', default='days', )

class MedicalHospitalBuilding(models.Model):
    _name = "medical.hospital.building"
    _description = "Medical hospital Building"

    name = fields.Char('Name',  required=True, help="Name of the building within the institution")
    institution = fields.Many2one('res.partner', 'Institution', domain=[('is_institution', '=', "1")],
                                  help="Medical Center")
    code = fields.Char('Code')
    extra_info = fields.Text('Extra Info')

class MedicalHospitalUnit(models.Model):
    _name = "medical.hospital.unit"
    _description = "Medical Hospital Unit"

    name = fields.Char('Name',  required=True, help="Name of the unit, eg Neonatal, Intensive Care, ...")
    institution = fields.Many2one('res.partner', 'Institution', domain=[('is_institution', '=', "1")],
                                  help="Medical Center")
    code = fields.Char('Code')
    extra_info = fields.Text('Extra Info')



class MedicalEquipment(models.Model):
    _name = "medical.equipment"
    _description = "Equipments / Job"

    name = fields.Char('Occupation',  required=True)
    code = fields.Char('Code')
    clinic = fields.Many2one('medical.clinic')
    treatment_ids = fields.Many2many('product.product', 'service_equipment_relation', 'service_id',
                                    'equipment_id', 'Services')

    patient_id = fields.Many2one('medical.patient', string='Patient',)
    appointment_id = fields.Many2one('medical.appointment', string='Appointment',)

    # appointment_date = fields.Datetime(related='appointment_id.appointment_date',string='Appointment Date',)
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(['|', ('name', operator, name), ('code', operator, name)])
        if not recs:
            recs = self.search([('name', operator, name)])
        return recs.name_get()

class ChartSelection(models.Model):
    _description = "teeth chart selection"
    _name = "chart.selection"

    type = fields.Selection(
        [('universal', 'Universal Numbering System'),
         ('palmer', 'Palmer Method'),
         ('iso', 'ISO FDI Numbering System')],
        'Select Chart Type', default='universal')



class ProductCategory(models.Model):
    _inherit = "product.category"
    _description = "Product Category"

    treatment = fields.Boolean('Treatment')

    def get_treatment_categs(self):
        all_records = self.search([])
        treatment_list = []
        for each_rec in all_records:
            if each_rec.treatment == True:
                treatment_list.append({'treatment_categ_id': each_rec.id, 'name': each_rec.name, 'treatments': []})

        product_rec = self.env['product.product'].search([('is_treatment', '=', True)])
        for each_product in product_rec:
            each_template = each_product.product_tmpl_id
            for each_treatment in treatment_list:
                if each_template.categ_id.id == each_treatment['treatment_categ_id']:
                    each_treatment['treatments'].append(
                        {'treatment_id': each_product.id, 'treatment_name': each_template.name,
                         'action': each_product.action_perform})
                    break

        return treatment_list


class PlannedVisitAlert(models.Model):
    _name = "planned.visit.alert"
    _description = "Planned Visit Alert"

    patient_name = fields.Many2one('medical.patient', 'Patient Name', readonly=True)
    treatment_name = fields.Many2one('product.product', 'Treatment Name', readonly=True)
    operated_date = fields.Datetime('Last Operated Date', readonly=True)



class MedicalDoseUnit(models.Model):
    _name = "medical.dose.unit"
    _description = " Medical Dose Unit"

    name = fields.Char('Unit',  required=True, )
    desc = fields.Char('Description')

    _sql_constraints = [
        ('dose_name_uniq', 'unique(name)', 'The Unit must be unique !'),
    ]

class MedicalDrugRoute(models.Model):
    _name = "medical.drug.route"
    _description = "Medical Drug Route"

    name = fields.Char('Route', required=True)
    code = fields.Char('Code', )

    _sql_constraints = [
        ('route_name_uniq', 'unique(name)', 'The Name must be unique !'),
    ]


class MedicalDrugForm(models.Model):
    _name = "medical.drug.form"
    _description = "Medical Drug Form"

    name = fields.Char('Form', required=True, )
    code = fields.Char('Code', )

    _sql_constraints = [
        ('drug_name_uniq', 'unique(name)', 'The Name must be unique !'),
    ]


class MedicalMedicinePrag(models.Model):
    _name = "medical.medicine.prag"
    _description = "Medical Medicine Prag"

    name = fields.Many2one('product.product', required=True, )
    code = fields.Char('Code', )
    price = fields.Float(related='name.lst_price')
    qty_available = fields.Float(related="name.qty_available", string="Quantity Available")

    _sql_constraints = [
        ('drug_name_uniq', 'unique(name)', 'The Name must be unique !'),
    ]

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.price = self.name.lst_price

    # @api.model
    # def create(self,vals):
    #     if 'name' in vals:
    #         if isinstance(vals['name'], str):
    #             product = self.env['product.product'].create({'name':vals['name']})
    #             if product:
    #                 vals.update({'name':product.id})
    #     result = super(MedicalMedicinePrag, self).create(vals)
    #     return result

    @api.model
    def name_create(self, name):
        if name:
            product_id = self.env['product.product'].sudo().create({'name': name})

            medical_medicine_prag_id = self.create({'name': product_id.id})
            return [(medical_medicine_prag_id.id)]

# MEDICATION DOSAGE
class MedicalMedicationDosage(models.Model):
    _name = "medical.medication.dosage"
    _description = "Medicament Common Dosage combinations"

    name = fields.Char('Frequency', help='Common frequency name', required=True, )
    code = fields.Char('Code', help='Dosage Code, such as SNOMED, 229798009 = 3 times per day')
    abbreviation = fields.Char('Abbreviation',
                               help='Dosage abbreviation, such as tid in the US or tds in the UK')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Unit already exists')]


class IrAttachment(models.Model):
    """
    Form for Attachment details
    """
    _inherit = "ir.attachment"
    _description = "Medical Attachments"

    patient_id = fields.Many2one('medical.patient', 'Patient')


# from odoo import fields, models
# class CalendarEvent(models.Model):
#     _name = 'calendar.event'
#     _description = 'Calendar Event'
#     name = fields.Char(string='Event Name', required=True)
#     start_date = fields.Datetime(string='Start Date', required=True)
#     end_date = fields.Datetime(string='End Date', required=True)
#     description = fields.Text(string='Description')
#     color = fields.Integer(string='Color Index')
#     recurrence = fields.Selection(
#         [('none', 'None'),
#          ('daily', 'Daily'),
#          ('weekly', 'Weekly'),
#          ('monthly', 'Monthly'),
#          ('yearly', 'Yearly')],
#         string='Recurrence',
#         default='none')