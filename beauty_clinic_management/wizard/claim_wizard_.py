from datetime import timedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64
import pytz
from datetime import datetime


class CalenderInvoiceWizard(models.TransientModel):
    _name = 'calender.invoice.wizard'
    _description = "calender.invoice.wizard"

    @api.model
    def default_get(self, fields):
        res = super(CalenderInvoiceWizard, self).default_get(fields)
        if self.env.context.get('default_appointment_id'):
            appointment_id = self.env['medical.appointment'].search([
                ('id', '=', self.env.context.get('default_appointment_id'))])
            service_ids = []
            total_amount = 0
            payment_due = appointment_id.payment_due
            for service in appointment_id.services_ids:
                service_ids.append((0, 0, {
                    'product_id': service.id,
                }))
                total_amount += service.lst_price
            res.update({
                'service_ids': service_ids,
                'patient_id': appointment_id.patient.id,
                'doctor_id': appointment_id.doctor.id,
                'clinic_id': appointment_id.clinic.id,
                'total_amount': total_amount,
                'payment_due': total_amount,  #payment_due + total_amount
                'current_payment': total_amount,
            })
        return res

    patient_id = fields.Many2one('medical.patient', 'Patient')
    doctor_id = fields.Many2one('medical.doctor', 'Doctor')
    clinic_id = fields.Many2one('medical.clinic', 'Clinic')
    service_ids = fields.One2many('app.service.line', 'wiz_invoice_line', string='Services')
    appointment_id = fields.Many2one('medical.appointment')
    total_amount = fields.Float('Total Fees')
    payment_due = fields.Float('Payment Due')
    current_payment = fields.Float('Current Payment')

    def action_create_invoice(self):
        if self.current_payment != self.total_amount:
            raise ValidationError(_('Current Payment must be same as Total Fees!'))
        invoice_obj = self.env['account.move']
        appointment = self.appointment_id
        prods_lines = []
        for line in self.service_ids:
            account_id = line.product_id.product_tmpl_id.property_account_income_id.id
            prods_lines.append((0, None, {
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'quantity': 1,
                'account_id': account_id,
                'partner_id': appointment.patient.partner_id.id,
                'price_unit': line.product_id.lst_price
            }))
        invoice_data = {
            'patient_id': appointment.patient.partner_id.id,
            'partner_id': appointment.patient.partner_id.id,
            'doctor': appointment.doctor.id,
            'clinic': appointment.clinic.id,
            'fiscal_position_id': appointment.patient.partner_id.property_account_position_id and appointment.patient.partner_id.property_account_position_id.id or False,
            'invoice_payment_term_id': appointment.patient.partner_id.property_payment_term_id and appointment.patient.partner_id.property_payment_term_id.id or False,
            'move_type': 'out_invoice',
            'invoice_line_ids': prods_lines
        }
        invoice_id = invoice_obj.create(invoice_data)
        invoice_id.action_post()
        self.appointment_id.invoice_id = invoice_id.id
        self.appointment_id.is_invoice_state = True
        self.appointment_id.invoice_state = 'invoiced'

        message_id = self.env['medical.notes.message'].create({'name': _("Invoice successfully created.")})
        # return {
        #     'name': _('Success'),
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'medical.notes.message',
        #     'res_id': message_id.id,
        #     'target': 'new'
        # }
        return {
            'name': _('Customer Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.appointment_id.invoice_id.id,
        }

        # For Payment Registration
        """
        journal_id = self.env['account.journal'].search(
            [('type', 'in', ['cash', 'bank']), ('company_id', '=', self.env.company.id)], limit=1)

        pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move', active_ids=invoice_id.ids).create({
            'payment_date': fields.Date.today(),
            'journal_id': journal_id.id,
            'amount': self.current_payment,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
        })
        pmt_wizard._create_payments()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
        """

        # action = {
        #     'view_mode': 'form',
        #     'res_model': 'account.move',
        #     'view_id': self.env.ref('account.view_move_form').id,
        #     'type': 'ir.actions.act_window',
        #     'res_id': invoice_id.id,
        #     'target': 'current'
        # }
        # return action


class CalenderPaymentWizard(models.TransientModel):
    _name = 'calender.payment.wizard'
    _description = "calender.payment.wizard"

    @api.model
    def default_get(self, fields):
        res = super(CalenderPaymentWizard, self).default_get(fields)
        if self.env.context.get('default_appointment_id'):
            amount = 0
            communication = ''
            appointment_id = self.env['medical.appointment'].search([
                ('id', '=', self.env.context.get('default_appointment_id'))])
            appointment_id.invoice_state = 'payment_registered'
            appointment_id.is_register_payment = True
            if appointment_id and appointment_id.invoice_id:
                amount = appointment_id.invoice_id.amount_residual
                communication = appointment_id.invoice_id.name
            res.update({
                'journal_id': self.env['account.journal'].search(
                    [('type', 'in', ['cash', 'bank']), ('company_id', '=', self.env.company.id)], limit=1),
                'amount': amount,
                'communication': communication
            })
        return res

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    journal_id = fields.Many2one('account.journal', store=True, readonly=False,
                                 domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]",
                                 string="Journal")
    partner_bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string="Recipient Bank Account",
        readonly=False,
        store=True,
    )
    amount = fields.Float(string="Amount")
    payment_date = fields.Date(string="Payment Date", required=True,
                               default=fields.Date.context_today)
    communication = fields.Char(string="Memo")
    appointment_id = fields.Many2one('medical.appointment')
    payment_method_line_id = fields.Many2one('account.payment.method.line')

    def action_create_payment(self):
        if self.appointment_id:
            pmt_wizard = self.env['account.payment.register'].with_context(active_model='account.move',
                                                                           active_ids=self.appointment_id.invoice_id.ids).create(
                {
                    'payment_date': self.payment_date,
                    'journal_id': self.journal_id.id,
                    'amount': self.amount,
                    'payment_method_line_id': self.payment_method_line_id.id,
                })
            pmt_wizard._create_payments()
            message_id = self.env['medical.notes.message'].create({'name': _("Payment successfully created.")})
            return {
                'name': _('Success'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'medical.notes.message',
                'res_id': message_id.id,
                'target': 'new'
            }


class CancelReasonWizard(models.TransientModel):
    _name = 'cancel.reason.wizard'
    _description = "Cancellation Reason"

    name = fields.Text('Reason')

    def action_cancel(self):
        cancel_obj = self.env['cancel.reason']
        for rec in self:
            cancel_obj.create({'name': rec.name})


class CalenderNotesWizard(models.TransientModel):
    _name = 'calender.notes.wizard'
    _description = "calender.notes.wizard"

    @api.model
    def default_get(self, fields):
        res = super(CalenderNotesWizard, self).default_get(fields)
        if self.env.context.get('default_appointment_id'):
            appointment_id = self.env['medical.appointment'].search([
                ('id', '=', self.env.context.get('default_appointment_id'))])
            note_lines = []
            for line in appointment_id.note_ids:
                note_lines.append((0, None, {
                    'user_id': line.user_id.id,
                    'last_notes': line.last_notes,
                    'update_notes': line.update_notes,
                    'update_date': line.create_date,
                }))
            res.update({
                'notes': appointment_id.comments,
                'is_notes': appointment_id.comments if appointment_id.comments else False,
                'note_ids': note_lines
            })
        return res

    notes = fields.Text('Notes')
    is_notes = fields.Boolean('Is Notes')
    edit_notes = fields.Boolean('Edit Notes')
    appointment_id = fields.Many2one('medical.appointment')
    note_ids = fields.One2many('medical.notes.wizard', 'note_id', 'Notes History')

    def action_create_notes(self):
        is_before_note = False
        if self.appointment_id.comments:
            is_before_note = True
        if self.notes != self.appointment_id.comments:
            notes = self.env['medical.notes.history'].create({
                'appointment_id': self.appointment_id.id,
                'user_id': self.env.user.id,
                'last_notes': self.appointment_id.comments,
                'update_notes': self.notes,
            })
        self.appointment_id.write({
            'comments': self.notes
        })
        if is_before_note:
            message_id = self.env['medical.notes.message'].create({'name': _("Notes edited successfully")})
        else:
            message_id = self.env['medical.notes.message'].create({'name': _("Notes added successfully")})
        return {
            'name': _('Successfull'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'medical.notes.message',
            'res_id': message_id.id,
            'target': 'new'
        }

    def action_edit_notes(self):
        self.write({
            'edit_notes': True
        })
        return {
            'name': 'Create: Notes',
            'view_mode': 'form',
            'view_id': False,
            'res_model': self._name,
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }


class MedicalNotesWizard(models.TransientModel):
    _name = "medical.notes.wizard"

    note_id = fields.Many2one('calender.notes.wizard')
    user_id = fields.Many2one('res.users')
    last_notes = fields.Text('Previous Notes')
    update_notes = fields.Text('Updated Notes')
    update_date = fields.Datetime('Updated Date')


class MedicalNotesMessage(models.TransientModel):
    _name = "medical.notes.message"

    name = fields.Text('Message')

    def action_submit(self):
        return {'type': 'ir.actions.act_window_close'}


class AppServiceLine(models.TransientModel):
    _name = 'app.service.line'
    _description = "app.service.line"

    product_id = fields.Many2one('product.product', 'Product')
    amount = fields.Float(related="product_id.lst_price", string='Fees')
    wiz_invoice_line = fields.Many2one('calender.invoice.wizard')


class CalenderAppointmentWizard(models.TransientModel):
    _name = 'calender.appointment.wizard'
    _description = "calender.appointment.wizard"

    @api.model
    def default_get(self, fields):
        # tz = self.env.user.tz
        tz = 'Asia/Qatar'
        res = super(CalenderAppointmentWizard, self).default_get(fields)
        if self.env.context.get('dateToString') and self.env.context.get('from_time'):
            str_date = datetime.strptime(self.env.context.get('dateToString'), "%a %b %d %Y %H:%M:%S %Z%z").date()
            str_date = str(str_date) + ' ' + self.env.context.get('from_time')
            datetime_object = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
            enddatetime_object = datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=30)
            local = pytz.timezone(tz)
            naive = datetime_object
            local_dt = local.localize(naive, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            appointment_sdate = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
            res['appointment_sdate'] = appointment_sdate
            from_time = datetime_object.strftime('%H:%M')
            split_data = from_time.split(':')
            res['from_time'] = (float(split_data[0]) * 60 + float(split_data[1])) / 60
            appointment_edate = utc_dt + timedelta(minutes=30)
            res['appointment_edate'] = appointment_edate.strftime("%Y-%m-%d %H:%M:%S")
            from_time = enddatetime_object.strftime('%H:%M')
            split_data = from_time.split(':')
            res['to_time'] = (float(split_data[0]) * 60 + float(split_data[1])) / 60
        # else:
        #     if self.env.context.get('default_appointment_sdate'):
        #         appointment_sdate = datetime.strptime(self.env.context.get('default_appointment_sdate'), '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone(tz))
        #         from_time = appointment_sdate.strftime('%H:%M')
        #         split_data = from_time.split(':')
        #         res['from_time'] = (float(split_data[0]) * 60 + float(split_data[1])) / 60
        #     if self.env.context.get('default_appointment_edate'):
        #         appointment_edate = datetime.strptime(self.env.context.get('default_appointment_edate'), '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone(tz))
        #         to_time = appointment_edate.strftime('%H:%M')
        #         split_data = to_time.split(':')
        #         res['to_time'] = (float(split_data[0]) * 60 + float(split_data[1])) / 60
        return res

    patient_id = fields.Many2one('medical.patient', 'Patient')
    mobile_number = fields.Char(related='patient_id.mobile', readonly=False, string='Mobile')
    qid = fields.Char(related='patient_id.qid', readonly=False, string='Qid')
    duration_id = fields.Many2one('duration.duration', 'Duration')

    from_time = fields.Float('From Time')
    to_time = fields.Float('To Time')

    doctor_id = fields.Many2one('medical.doctor',compute='_compute_doctor', string='Doctor')
    clinic_id = fields.Many2one('medical.clinic', 'Clinic')

    procedure_ids = fields.Many2many('medical.procedure', 'wiz_process_rel', 'appointment_id', 'process_id',
                                     'Initial Procedures')

    service_ids = fields.Many2many('product.product', string='Services')
    amount = fields.Float(compute='_compute_amount', default=0.0, string='Amount')

    appointment_sdate = fields.Datetime('Appointment Start')
    appointment_edate = fields.Datetime('Appointment End')
    appointment_id = fields.Many2one('medical.appointment')

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id and self.patient_id.mobile:
            self.mobile_number = self.patient_id.mobile

    @api.onchange('patient_id')
    def onchange_mobile(self):
        if self.patient_id and self.patient_id.mobile:
            self.patient_id = self.env['medical.patient'].search([('mobile', '=', self.mobile_number)]).id

    @api.onchange('mobile_number')
    def onchange_mobile_number(self):
        if self.mobile_number:
            patient = self.env['medical.patient'].search([('mobile', '=', self.mobile_number)], limit=1)
            if patient:
                self.patient_id = patient.id

    # Appointment service amount computed and changes when Selecting Service

    # @api.onchange('service_ids')
    # def _compute_clinic_ids(self):
    #     for rec in self:
    #         if rec.clinic_id:
    #             clinic_ids = []
    #             for clinic in rec.clinic_ids:
    #                 clinic_ids = self.env['product.product'].search([('clinic_ids', 'in', rec.clinic_id.id)]).ids
    #             rec.clinic_ids = [(6, 0, clinic_ids)]

    @api.depends('clinic_id')
    @api.onchange('clinic_id')
    def _compute_doctor(self):
        for rec in self:
            if rec.clinic_id and rec.clinic_id.doctor_id:
                rec.doctor_id = rec.clinic_id.doctor_id.id

    @api.depends('service_ids')
    @api.onchange('service_ids')
    def _compute_amount(self):
        for rec in self:
            if rec.service_ids:
                amount = 0.0
                for service_id in rec.service_ids:
                    amount += service_id.lst_price
                rec.amount = amount

    @api.onchange('service_ids', 'appointment_sdate')
    def calculate_enddate(self):
        if self.appointment_sdate and self.service_ids:
            duration = 0.0
            amount = 0.0
            for service_id in self.service_ids:
                duration += int(service_id.duration_id.duration_name)
                amount += service_id.lst_price
        else:
            duration = 30
        self.appointment_edate = self.appointment_sdate + timedelta(minutes=duration)
        # tz = self.env.user.tz
        tz = 'Asia/Qatar'
        appointment_edate = self.appointment_edate.astimezone(pytz.timezone(tz))
        to_time = appointment_edate.strftime('%H:%M')
        split_data = to_time.split(':')
        self.to_time = (float(split_data[0]) * 60 + float(split_data[1])) / 60

        appointment_sdate = self.appointment_sdate.astimezone(pytz.timezone(tz))
        from_time = appointment_sdate.strftime('%H:%M')
        s_split_data = from_time.split(':')
        self.from_time = (float(s_split_data[0]) * 60 + float(s_split_data[1])) / 60

    def action_edit(self):
        self.appointment_id.write({
            'patient': self.patient_id.id,
            'doctor': self.doctor_id.id,
            'clinic': self.clinic_id.id,
            'appointment_sdate': self.appointment_sdate,
            'appointment_edate': self.appointment_edate,
            'services_ids': [(6, 0, self.service_ids.ids)]
        })
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def action_create(self):
        appointment_validation = self.env['medical.appointment'].search([
            ('clinic', '=', self.clinic_id.id), ('appointment_sdate', '=', self.appointment_sdate,)])
        if appointment_validation:
            raise ValidationError('Already Booked Appointment')
        else:
            app_id = self.env['medical.appointment'].create({
                'patient': self.patient_id.id,
                'doctor': self.doctor_id.id,
                'clinic': self.clinic_id.id,
                'appointment_sdate': self.appointment_sdate,
                # 'appointment_sdate': self.appointment_sdate - timedelta(hours=5,minutes=30),
                'appointment_edate': self.appointment_edate,
                # 'appointment_edate': self.appointment_edate - timedelta(hours=5,minutes=30),
                'duration_id': self.duration_id.id,
                'services_ids': [(6, 0, self.service_ids.ids)]
            })
            self.appointment_id = app_id.id
        # message_id = self.env['medical.notes.message'].create({'name': _("Appointment created successfully")})
        # return {
        #     'name': _('Successfull'),
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'medical.notes.message',
        #     'res_id': message_id.id,
        #     'target': 'new'
        # }
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

        # action = {
        #     'view_mode': 'form',
        #     'res_model': 'calender.appointment.wizard',
        #     'type': 'ir.actions.act_window',
        #     'target': 'new',
        #     'context': {'recordCreated': 'created'}
        # }
        action = {
            'name': _(' '),
            'view_mode': 'calendar',
            'res_model': 'medical.appointment',
            'view_id': self.env.ref('beauty_clinic_management.view_medical_appointment').id,
            'type': 'ir.actions.act_window',
            'context': {'default_appointment_sdate': self.appointment_sdate.date()},
            'target': 'current'
        }
        return action
    #
    # def reload_page(self):
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }


class ClaimWizard(models.TransientModel):
    _name = 'dental.claim.wizard'
    _description = "Dental Claim wizard"

    to_date = fields.Date(string='To Date')
    from_date = fields.Date(string='From Date')

    def print_report(self):
        datas = {'active_ids': self.env.context.get('active_ids', []),
                 'form': self.read(['to_date', 'from_date'])[0],
                 }
        values = self.env.ref('beauty_clinic_management.claim_report_qweb').report_action(self, data=datas)
        return values

    def generate_backlog_excel_report(self):
        import sys, os
        import xlsxwriter
        # Create an new Excel file and add a worksheet.
        # workbook = xlsxwriter.Workbook('/opt/odoo/backlog_demo.xlsx')
        # workbook = xlsxwriter.Workbook('/home/pragmatic/Downloads/%s.xlsx'%self.from_date)
        script_dir = os.path.dirname(__file__)  # Create a relative path to the Downloads folder
        relative_path = os.path.join(script_dir, f'{self.from_date}.xlsx')
        workbook = xlsxwriter.Workbook(relative_path)
        worksheet = workbook.add_worksheet()
        # Add a font format to use to highlight cells.
        bold = workbook.add_format({'size': 10})
        normal = workbook.add_format({'size': 10})
        r = 0
        c = 0
        data_list = []
        output_header = ['Patient Name', 'MEM ID', 'Date of Birth', 'Nationality', 'Country of Residence',
                         'Sex', 'Mobile', 'Invoice Number', 'Healthcare Professional',
                         'Healthcare Professional ID', 'Healthcare Professional Type', 'Episode Number',
                         'Clinic', 'Appointment Start', 'Appointment End', 'Treatment', 'Treatment Code']
        for item in output_header:
            worksheet.write(r, c, item, bold)
            c += 1
        #         picking_type_ids = self.env['stock.picking.type'].search(['|', ('name', 'ilike', 'Delivery order'), ('name', 'ilike', 'dropship')])
        #
        #
        #         picking_ids = self.env['stock.picking'].search([('state', '!=', 'done'),('state', '!=', 'cancel'), ('picking_type_id', 'in', picking_type_ids.ids)])
        #
        #         for picking in picking_ids: #[:5]:
        #             for line in picking.move_lines_related:
        #                 line_list = []
        #
        #                 line_list.append(picking.name)
        #
        #     #             appending name
        #                 if picking.sale_id.partner_id :
        #                     line_list.append(picking.sale_id.partner_id.name)
        #                 else:
        #                     line_list.append('')
        #
        #     #            if a sale order is associated with the picking
        #                 if picking.sale_id :
        #                     line_list.append(picking.sale_id.name)
        #                     if picking.sale_id.client_order_ref:
        #                         line_list.append(picking.sale_id.client_order_ref)
        #                     else:
        #                         line_list.append('')
        # #                     line_list.append(picking.sale_id.date_order)
        #
        #                     t_date= datetime.datetime.strptime(picking.sale_id.date_order, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
        #                     line_list.append(t_date)
        #
        #                 else :
        #                     line_list.append('')
        #                     line_list.append('')
        #                     line_list.append('')
        #
        #                 if picking.purchase_id:
        #                     line_list.append(picking.purchase_id.name)
        #                     line_list.append(picking.purchase_id.partner_id.name)
        # #                     line_list.append(picking.purchase_id.date_order)
        #                     t_date= datetime.datetime.strptime(picking.purchase_id.date_order, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
        #                     line_list.append(t_date)
        #
        #                 else:
        #                     line_list.append('')
        #                     line_list.append('')
        #                     line_list.append('')
        #
        #                 line_list.append(line.product_id.default_code)
        # #                 line_list.append(line.product_id.default_code)
        #
        # #                 if picking is attached to a PO / code for product decription
        #                 if picking.purchase_id:
        #                     flag = False
        # #                     if refrence to purchase order line exists
        #                     if line.purchase_line_id:
        #                         flag = True
        #                         line_list.append(line.purchase_line_id.name)
        # #                         else iterate through all lines in the po
        #                     else :
        #                         for po_line in picking.purchase_id:
        #                             if po_line.product_id.id == line.product_id.id:
        #                                 flag = True
        #                                 line_list.append(po_line.name)
        #                         if flag == False:
        #                             line_list.append('')
        # #                 if no PO fetch price from SO
        #                 elif picking.sale_id :
        #                     flag = False
        #                     for so_line in picking.sale_id.order_line:
        #                         if so_line.product_id.id == line.product_id.id:
        #                             flag = True
        #                             line_list.append(so_line.name)
        #                     if flag == False:
        #                             line_list.append('')
        #                 else:
        #                     line_list.append('')
        #
        #                 line_list.append(line.product_uom_qty)
        #
        #
        # #                 if picking is attached to a PO / code for unit price
        #                 if picking.purchase_id:
        # #                     if refrence to purchase roder line exists
        #                     if line.purchase_line_id:
        #                         line_list.append(line.purchase_line_id.price_unit)
        # #                         else iterate through all lines in the po
        #                     else :
        #                         for po_line in picking.purchase_id:
        #                             if po_line.product_id.id == line.product_id.id:
        #                                 line_list.append(po_line.price_unit)
        # #                 if no PO fetch price from SO
        #                 elif picking.sale_id :
        #                     for so_line in picking.sale_id.order_line:
        #                         if so_line.product_id.id == line.product_id.id:
        #                             line_list.append(so_line.price_unit)
        #                 else:
        #                     line_list.append(line.product_id.lst_price)
        #
        #                 data_list.append(line_list)
        #
        inv_data = self.env['account.move'].search([
            ('invoice_date', '>=', self.from_date), ('invoice_date', '<=', self.to_date), ('patient', '!=', False)
        ])
        for inv in inv_data:
            data = []
            data.append(inv.patient.name.name)
            if inv.patient.name.ref:
                data.append(inv.patient.name.ref)
            else:
                data.append('')
            if inv.patient.dob:
                data.append(inv.patient.dob)
            else:
                data.append('')
            if inv.patient.nationality_id:
                data.append(inv.patient.nationality_id.name)
            else:
                data.append('')
            if inv.patient.name.country_id:
                data.append(inv.patient.name.country_id.name)
            else:
                data.append('')
            if inv.patient.sex:
                if inv.patient.sex == 'm':
                    data.append('Male')
                else:
                    data.append('Female')
            else:
                data.append('')
            if inv.patient.mobile:
                data.append(inv.patient.mobile)
            else:
                data.append('')
            if inv.number:
                data.append(inv.number)
            else:
                data.append('')
            if inv.clinic:
                data.append(inv.clinic.name.name)
            else:
                data.append('')
            if inv.clinic.code:
                data.append(inv.clinic.code)
            else:
                data.append('')
            if inv.clinic.speciality:
                data.append(inv.clinic.speciality.name)
            else:
                data.append('')
            if inv.patient.apt_id:
                apt_line = []
                clinic_line = []
                app_start = []
                app_end = []
                for apt in inv.patient.apt_id:
                    if apt:
                        apt_line.append(apt.name)
                        if apt.clinic:
                            clinic_line.append(apt.clinic.name.name)
                        else:
                            clinic_line.append('')
                        if apt.appointment_sdate:
                            app_start.append(apt.appointment_sdate)
                        else:
                            app_start.append('')
                        if apt.appointment_edate:
                            app_end.append(apt.appointment_edate)
                        else:
                            app_end.append('')
                    else:
                        apt_line.append('')
                data.append('1402')  #apt_line)
                data.append('Arshad')  #clinic_line)
                data.append('06/06/2018')  #app_start)
                data.append('06/06/2018')  #app_end)
            else:
                data.append('')
                data.append('')
                data.append('')
                data.append('')
            if inv.invoice_line_ids:
                product = []
                p_code = []
                for line in inv.invoice_line_ids:
                    product.append(line.product_id.name)
                    if line.product_id.default_code:
                        p_code.append(line.product_id.default_code)
                    else:
                        p_code.append('')
                data.append('Product1')  #product)
                data.append('P00000112')  #p_code)
            else:
                data.append('')
                data.append('')

            data_list.append(data)

        #         data_list = [['1','2'],['1','GFHC'],['22','adygb']]
        r += 1
        for data in data_list:
            c = 0
            for item in data:
                worksheet.write(r, c, item, normal)
                c += 1
            r += 1

        workbook.close()
#         data = base64.b64encode(open('/tmp/%s.xlsx'%self.from_date,'rb').read())
