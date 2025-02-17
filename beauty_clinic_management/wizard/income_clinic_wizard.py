# -*- coding: utf-8 -*-
import time
from odoo import fields, models, api,_
from odoo.exceptions import UserError

class income_by_clinic_report_wizard(models.TransientModel):
    _name='income.by.clinic.report.wizard'
    _description = "Invoice By Clinic WiZard"
   
    start_date = fields.Date('Start Date',required=True)
    end_date = fields.Date('End Date',required=True)
    
    def income_by_clinic_report(self):
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        return self.env.ref('beauty_clinic_management.income_byreport_report12333').report_action(self, data=data)


class patient_by_clinic_report_wizard(models.TransientModel):
    _name='patient.by.clinic.report.wizard'
    _description = "Patient By Clinic Report Wizard"
   
    start_date = fields.Date('Start Date',required=True)
    end_date = fields.Date('End Date',required=True)
    
    def patient_by_clinic_report(self):
        datas = {'active_ids': self.env.context.get('active_ids', []),'form':self.read(['start_date', 'end_date'])[0]}
        values=self.env.ref('beauty_clinic_management.patient_byreport_report12333').report_action(self, data=datas)
        return values