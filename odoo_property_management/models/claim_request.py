# -*- coding: utf-8 -*-
################################################################################
#
#    AAHB-Service Co.Ltd (https://www.3bdalla3adil.github.io)
#    Author: ABDULLA BASHIR
#
################################################################################

from odoo import models, fields, api
from odoo.osv import expression

#=============================================================================
#==== PIPELINE ============ Claim Request ==> Property Details ==> ... =======
#=============================================================================

#ToDo:Crafted custom claim request ==> integrate with Maintenance Module


class ClaimRequest(models.Model):
    _name = 'claim.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']  #'crm.lead'
    _description = 'Claim Request'
    _rec_name = 'claim_no'
    _order = 'claim_no desc'

    # @api.model
    # def _get_view(self, view_id=None, view_type='tree', **options):
    #     arch, view = super()._get_view(view_id, view_type, **options)
    #     user = self.env.user.name
    #     if view_type == 'tree' and user != 'ISMAIL':
    #         for node in arch.xpath("//field[@name='work_evaluation']"):
    #             node.set('invisible', '1')
    #             node.set('widget', 'selection')
    #     if view_type == 'tree' and user == 'ISMAIL':
    #         for node in arch.xpath("//field[@name='remarks']"):
    #             node.set('optional', 'hide')
        # return arch, view

    @api.model
    def create(self, vals):
        if vals.get('claim_no', 'New') == 'New':
            from datetime import datetime
            seq_date = datetime.now().strftime('%Y')
            seq = self.env['ir.sequence'].next_by_code('claim.request') or '/'
            vals['claim_no'] = f'{seq_date}/{seq}'
            # vals['claim_no'] = seq
            claim = super(ClaimRequest, self).create(vals)
            # self._create_man_hours_lines()
            return claim

    # @api.model
    # def _get_current_month_range(self):
    #     """
    #     Calculate the date range for the current month.
    #     """
    #     today = fields.Date.today()
    #     current_month = today.month # without ()
    #     current_year = today.year # without ()
    #
    #     first_day = today.replace(day=1,month=current_month,year=current_year)
    #     last_day = today
    #     return first_day, last_day
    #
    # def search(self, domain, offset=0, limit=None, order=None, count=False):
    #     """
    #     Override search to filter records based on the custom conditions:
    #     1. Claims in states `new`, `scheduled`, `in_progress`.
    #     2. Claims in `done` state limited to the current month.
    #     """
    #     context = self.env.context or {}
    #     if context.get('custom_filter'):
    #         first_day, last_day = self._get_current_month_range()
    #
    #         # Custom domain for the conditions
    #         custom_domain = [
    #             '|',
    #             ('state', 'in', ['new', 'scheduled', 'in_progress']),
    #             '&',
    #             ('state', '=', 'done'),
    #             ('claim_dat', '>=', first_day),
    #             ('claim_dat', '<=', last_day),
    #         ]
    #
    #         # Combine the existing domain with the custom one
    #
    #         domain = expression.AND([domain, custom_domain])
    #
    #     # Call the original search method
    #     return super(ClaimRequest, self).search(domain, offset, limit, order, count)

    #===============================COMMENTED FOR PRODUCTION============================
    # def write(self, vals):
    #     res = super(ClaimRequest, self).write(vals)
    #     if 'assigned_to' in vals:
    #         self._create_man_hours_lines()
    #     return res
    #========================================================================================

    @api.depends('unit', 'claim_type_id', 'group')
    @api.onchange('unit', 'claim_type_id', 'group')
    def _compute_claims(self):
        claim_obj = self.env['claim.request']
        for rec in self:
            if rec:
                rec.claim_ids = claim_obj.search([
                    ('unit', '=', rec.unit.id),
                    ('claim_type_id', '=', rec.claim_type_id.id),
                    ('group', '=', rec.group),
                    ('claim_no', '!=', rec.claim_no),
                ])
    # =========================COMMENTED FOR PRODUCTION=============================================
    # @api.depends('material_ids.total_cost', 'man_hours_ids.total_cost')
    # def _compute_transportation_fee(self):
    #     for rec in self:
    #         total_material_cost = sum(material.total_cost for material in rec.material_ids)
    #         total_man_hours_cost = sum(man_hour.total_cost for man_hour in rec.man_hours_ids)
    #         rec.total_material_cost = total_material_cost
    #         rec.total_man_hours_cost = total_man_hours_cost
    #         rec.transportation_fee = (total_material_cost + total_man_hours_cost) * 0.20
    #==================================================================================================
    # def notify_the_world(self,vals):

    #     users = self.env['res.users'].search([('company_id', '=', self.env.user.company_id.id)])
    #     for claim in self:
    #         for user in users:
    #             user.notify_warning(f"Claim Reference [{claim.claim_no}] state has been changed to {vals['state']}.")

    # @api.model
    # def write(self, vals):
    #     self.notify_the_world(vals)
    #     return super(ClaimRequest,self).write(vals)

    claim_ids = fields.Many2many('claim.request', relation='rel_claims_request', compute='_compute_claims',
                                 required=False, tracking=True)

    claim_no = fields.Char(string="Claim No.", required=False, tracking=True)

    claim_date = fields.Datetime(string="Claim Date", required=False, tracking=True, default=fields.Datetime.now)
    claim_dat = fields.Date(compute='_compute_date', string="Claim Date", store=True, tracking=True, )

    claim_type_id = fields.Many2one(comodel_name="claim.type",
                                    string="Claim Type", required=False, tracking=True)

    state_id = fields.Many2one('claim.state', string="Claim Status", required=False, tracking=True, )
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('scheduled', 'Scheduled'),
        ('in_progress', 'IN Progress'),
        ('done', 'Completed'),
    ], string="Claim Status", required=False, tracking=True, default='new')

    priority = fields.Selection([('1', 'Urgent'), ('2', 'Normal')], string="Priority", default='2', required=False, tracking=True, )
    unit = fields.Many2one(comodel_name="property.unit", string="Unit", required=False, tracking=True, )

    description = fields.Text(string="Description", required=False, tracking=True, )
    group = fields.Selection([('a', 'A'), ('b', 'B'), ], string="Group",default='b', required=False, tracking=True, )
    checked_by = fields.Many2one(comodel_name="hr.employee", compute='_set_check_by', string="Checked By",
                                 required=False, tracking=True, )
    assigned_to = fields.Many2many(comodel_name="hr.employee", string="Assigned To", required=False, tracking=True, )

    remarks_of_works = fields.Char(string="Remarks Of Works", required=False, tracking=True, )
    # assign_date = fields.Date(string="Assign Date", required=False, tracking=True, )
    assign_date = fields.Date(string="Reschedule Date", required=False, tracking=True, )
    actual_complete = fields.Date(string="Actual Complete", required=False, tracking=True)

    actual_time_done = fields.Float(string="Actual Time Done", required=False, tracking=True, )
    customer_feedback = fields.Char(string="Customer Feedback", required=False, tracking=True, )
    # Added Customer Satisfaction Field
    work_evaluation = fields.Selection([('0', 'Very Bad'),
                                        ('1', 'Bad'),
                                        ('2', 'Acceptable'),
                                        ('3', 'Excellent')], string="Work Evaluation", tracking=True, )
    actual_cost = fields.Float(string="Actual Cost", required=False, tracking=True, )
    user_id = fields.Many2one(comodel_name="res.users", string="User",#,compute='_get_user'
                              default=lambda self: self.env.user, tracking=True, store=True)
    remarks = fields.Char(string="Remarks", required=False, tracking=True, )
    mobile = fields.Char(string="Mobile", related='unit.contract_id.mobile', tracking=True, store=True )

    company_id = fields.Many2one('res.company')

    #=================NEW ADDED FIELDS Commented for production=============================
    # invoice_id = fields.Many2one('account.move', 'Invoice')
    # invoiced = fields.Boolean(default=False)
    #
    #
    # man_hours_ids = fields.One2many('claim.request.man.hours', 'claim_id', string="Man-hours Consumption")
    # material_ids = fields.One2many('claim.request.material', 'claim_id', string="Material Consumption")
    # total_material_cost = fields.Float(string="Total Material Cost", compute='_compute_transportation_fee', store=True)
    # total_man_hours_cost = fields.Float(string="Total Man-hours Cost", compute='_compute_transportation_fee',
    #                                     store=True)
    # transportation_fee = fields.Float(string="Transportation Fee", compute='_compute_transportation_fee', store=True)

    # def action_revert(self):
    #     pass
    #
    # def create_invoice(self):
    #     pass

    # @api.onchange('assigned_to')
    # def _create_man_hours_lines(self):
    #     for claim in self:
    #         # check if technician already in the mans_hours_lines
    #         if not self.env['claim.request.man.hours'].search([('claim_id','=', claim.id),
    #                                                            ('employee_id','in', claim.assigned_to.ids)]):
    #             for employee in claim.assigned_to.ids:
    #                 self.env['claim.request.man.hours'].sudo().create({'claim_id': claim.id,
    #                                                                    # 'employee_id': employee.id,
    #                                                                    'employee_id': employee,
    #                                                                    })
    #==================================================================================================

    def _get_user(self):
        for rec in self:
            rec.user_id = self.env.user#.strftime('%d-%m-%Y')


    @api.depends('claim_date')
    def _compute_date(self):
        for rec in self:
            rec.claim_dat = rec.claim_date.date()#.strftime('%d-%m-%Y')

    @api.onchange('group')
    def _set_check_by(self):
        employee_obj = self.env['hr.employee']
        for rec in self:
            if rec.group == 'a':
                rec.checked_by = employee_obj.search([('name', 'ilike', 'yassen')]).id
            else:
                pass
                #rec.checked_by = employee_obj.search([('name', 'ilike', 'Bassam')]).id
# ==============================COMMENTED FOR PRODUCTION==============================================
#
# class ClaimRequestManHours(models.Model):
#     _name = 'claim.request.man.hours'
#     _description = 'Claim Request Man Hours'
#
#     claim_id = fields.Many2one('claim.request', string="Claim Request", required=False, ondelete='cascade')
#     date = fields.Date(string="Date", default=fields.Date.today, required=False)
#     employee_id = fields.Many2one('hr.employee', string="Employee Name", required=True)
#     employee_job = fields.Char(related='employee_id.job_id.name', string="Employee Job", readonly=True)
#     start_time = fields.Datetime(string="Start Time", default=fields.Datetime.now, required=False)
#     end_time = fields.Datetime(string="End Time", required=False)
#     total_hours = fields.Float(string="Hours Worked", compute='_compute_total_hours', store=True)
#     # hourly_rate = fields.Float(string="Rate per Hour", required=True , )
#     hourly_rate = fields.Float(string="Rate per Hour", required=False, default=16.85)
#     total_cost = fields.Float(string="Total Cost", compute='_compute_total_cost', store=True)
#
#     #transportation_fee = fields.Float(string="Transportation Fee", compute='_compute_transportation_fee', store=True)
#     # task_description = fields.Char(string="Task Description", required=True)
#
#     @api.depends('start_time', 'end_time')
#     def _compute_total_hours(self):
#         for rec in self:
#             if rec.start_time and rec.end_time:
#                 delta = rec.end_time - rec.start_time
#                 rec.total_hours = delta.total_seconds() / 3600.0
#
#     @api.depends('total_hours', 'hourly_rate')
#     def _compute_total_cost(self):
#         for worker_hour in self:
#             worker_hour.total_cost = worker_hour.total_hours * worker_hour.hourly_rate

    # @api.depends('total_cost')
    # def _compute_transportation_fee(self):
    #     for worker_hour in self:
    #         worker_hour.transportation_fee = worker_hour.total_cost * 0.20

#======================COMMENTED FOR PRODUCTION===================================================
# class ClaimRequestMaterial(models.Model):
#     _name = 'claim.request.material'
#     _description = 'Claim Request Material'
#
#     claim_id = fields.Many2one('claim.request', string="Claim Request", required=True, ondelete='cascade')
#     date = fields.Date(string="Date", default=fields.Date.today, required=True)
#     material_description = fields.Char(string="Description", required=True)
#     quantity_used = fields.Float(string="Quantity", required=True)
#     uom_id = fields.Many2one('uom.uom', string="Unit of Measure", required=True)
#     unit_cost = fields.Float(string="Rate", required=True)
#     total_cost = fields.Float(string="Total Cost", compute='_compute_total_cost', store=True)
#     # transportation_fee = fields.Float(string="Transportation Fee", compute='_compute_transportation_fee', store=True)
#     remark = fields.Char(string="Remark")
#
#     @api.depends('quantity_used', 'unit_cost')
#     def _compute_total_cost(self):
#         for material in self:
#             material.total_cost = material.quantity_used * material.unit_cost

    # @api.depends('total_cost')
    # def _compute_transportation_fee(self):
    #     for material in self:
    #         material.transportation_fee = material.total_cost * 0.20
#===================================================================================================================



class ClaimType(models.Model):
    _name = 'claim.type'
    _description = 'Claim Type'

    name = fields.Char(string="name", required=False, )


class ClaimState(models.Model):
    """ Model for case stages. This models the main stages of a Maintenance Request management flow. """

    _name = 'claim.state'
    _description = 'Claim State'
    # _order = 'sequence, id'

    name = fields.Char(string="name", required=False,translate=True )
    # =========================Commented for PRODUCTION===================
    # sequence = fields.Integer('Sequence', default=20)
    # fold = fields.Boolean('Folded in Claim Pipe')
    # done = fields.Boolean('Request Done')
    #===========================COMMENTED FOR PRODUCTION==================


# class MaintenanceRequest(models.Model):
#     _inherit = 'maintenance.request'
#
#     @api.onchange('unit', 'claim_type_id', 'group')
#     def _onchange_claim_details(self):
#         claim_obj = self.env['maintenance.request']
#         for rec in self:
#             if rec:
#                 rec.claim_ids = claim_obj.search([
#                     ('unit', '=', rec.unit.id),
#                     ('claim_type_id', '=', rec.claim_type_id.id),
#                     ('group', '=', rec.group),
#                     ('claim_no', '!=', rec.claim_no),
#                 ])
#
#     @api.onchange('group')
#     def _set_check_by(self):
#         employee_obj = self.env['hr.employee']
#         for rec in self:
#             if rec.group == 'a':
#                 rec.checked_by = employee_obj.search([('name', '=', 'Yassen')]).id
#             else:
#                 rec.checked_by = employee_obj.search([('name', '=', 'Bassam')]).id
#
#     claim_ids = fields.Many2many(comodel_name='maintenance.request', relation='rel_maintenance_request', required=False, tracking=True)
#     claim_no = fields.Char(string="Claim No.", required=False, tracking=True)
#     claim_type_id = fields.Many2one(comodel_name="claim.type", string="Claim Type", required=False, tracking=True)
#     state = fields.Selection(selection=[
#         ('new', 'New'),
#         ('scheduled', 'Scheduled'),
#         ('in_progress', 'In Progress'),
#         ('done', 'Completed'),
#     ], string="Claim Status", required=False, tracking=True, default='new')
#     claim_date = fields.Datetime(string="Claim Date", required=False, tracking=True, default=fields.Date.context_today)
#     unit = fields.Many2one(comodel_name="property.unit", string="Unit", required=False, tracking=True)
#     group = fields.Selection([('a', 'A'), ('b', 'B')], string="Group", required=False, tracking=True)
#     remarks_of_works = fields.Char(string="Remarks Of Works", required=False, tracking=True)
#     customer_feedback = fields.Char(string="Customer Feedback", required=False, tracking=True)
#     remarks = fields.Char(string="Remarks", required=False, tracking=True)


# class MaintenanceRequest(models.Model):
#     _inherit = 'maintenance.request'
#
# @api.depends('unit', 'claim_type_id', 'group')
# @api.onchange('unit', 'claim_type_id', 'group')
# def _onchange_claim_details(self):
#     claim_obj = self.env['maintenance.request']
#     for rec in self:
#         if rec:
#             rec.claim_ids = claim_obj.search([
#                 ('unit', '=', rec.unit.id),
#                 ('claim_type_id', '=', rec.claim_type_id.id),
#                 ('group', '=', rec.group),
#                 ('claim_no', '!=', rec.claim_no),
#             ])
#
# @api.onchange('group')
# def _set_check_by(self):
#     employee_obj = self.env['hr.employee']
#     for rec in self:
#         if rec.group == 'a':
#             rec.checked_by = employee_obj.search([('name', '=', 'Yassen')]).id
#         else:
#             rec.checked_by = employee_obj.search([('name', '=', 'Bassam')]).id
#
#     claim_ids = fields.Many2many(comodel_name='maintenance.request',relation='rel_maintenance_request', required=False, tracking=True)
#
#     claim_no = fields.Char(string="Claim No.", required=False, tracking=True)
#
#     claim_type_id = fields.Many2one(comodel_name="claim.type",
#                                     string="Claim Type", required=False, tracking=True)#replace maintenance_type
#     state = fields.Selection(selection=[
#         ('new', 'New'),
#         ('scheduled', 'Scheduled'),
#         ('in_progress', 'IN Progress'),
#         ('done', 'Completed'),
#     ], string="Claim Status", required=False, tracking=True, default='new') #replace stage_id
#
#     claim_date = fields.Datetime(string="Claim Date",
#                                  required=False, tracking=True, default=fields.Date.context_today)#replace request_date
#     claim_dat = fields.Date(string="Claim Date",
#                                  required=False, tracking=True, default=fields.Date.context_today)#replace request_date
#     unit = fields.Many2one(comodel_name="property.unit", string="Unit", required=False, tracking=True, )
#
#     group = fields.Selection([('a', 'A'), ('b', 'B'), ], string="Group", required=False, tracking=True, )
#     # checked_by = fields.Many2one(comodel_name="hr.employee", compute='_set_check_by', string="Checked By",
#     #                              required=False, tracking=True, )# maintenance_team_id
#
#     remarks_of_works = fields.Char(string="Remarks Of Works", required=False, tracking=True, )
#     # assign_date = fields.Date(string="Assign Date", required=False, tracking=True, )#schedule_date replace
#     # actual_complete = fields.Date(string="Actual Complete", required=False, tracking=True) #duration
#
#     # actual_time_completed = fields.Float(string="Actual Time Completed", required=False, tracking=True, )#duration replace
#     customer_feedback = fields.Char(string="Customer Feedback", required=False, tracking=True, )
#     # actual_cost = fields.Float(string="Actual Cost", required=False, tracking=True, )
#     # user_id = fields.Many2one(comodel_name="res.users", string="User",
#     #                           default=lambda self: self.env.user, tracking=True, )
#     remarks = fields.Char(string="Remarks", required=False, tracking=True, )

# @api.depends('course_ids')
# def _compute_progress(self):
#     for plan in self:
#         completed_courses = len(plan.course_ids.filtered(lambda c: c in plan.employee_id.training_record_ids.mapped('course_id')))
#         total_courses = len(plan.course_ids)
#         plan.progress = (completed_courses / total_courses) * 100 if total_courses > 0 else 0
#
#
# def _notify_overdue_training(self):
#     today = fields.Date.today()
#     overdue_plans = self.search([('due_date', '<', today), ('progress', '<', 100)])
#     for plan in overdue_plans:
#         template = self.env.ref('odoo_employee_training.email_template_overdue_training')
#         self.env['mail.template'].browse(template.id).send_mail(plan.id)
