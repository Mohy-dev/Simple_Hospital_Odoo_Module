from odoo import models, fields


class HmsPatient(models.Model):
    _name = "hms.patient"
    
    first_name = fields.Char(string = "First name")
    last_name = fields.Char(string = "Last name") 
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([("A+","A+"), ("A-","A-"), ("B+","B+"), ("B-","B-"), ("O+","O+"), ("O-","O-")], default="A+")
    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Char(string = "Address")
    age = fields.Integer()
    department_id = fields.Many2one("hms.department")
    doctors = fields.Many2many("hms.doctor")
    logs = fields.One2many("hms.logs", "patient_id")
    capacity = fields.Integer("Number of Patients", related = "department_id.capacity")