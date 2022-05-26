from odoo import models, fields, api


class Department(models.Model):
    _name = "hms.department"
    
    name = fields.Text()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', inverse_name='department_id', string="Patients")
    capacity = fields.Integer("Number of patients", default = 0)