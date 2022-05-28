from odoo import models, fields, api, exceptions
from datetime import date
from odoo.exceptions import UserError
from datetime import date , datetime,timedelta

import re

class HmsPatient(models.Model):
    _name = "hms.patient"
    
    first_name = fields.Char(string = "First name")
    last_name = fields.Char(string = "Last name")
    email = fields.Text(required=True)
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
    department_open = fields.Boolean(related='department_id.is_opened')
    
    def next_state(self):
        if self.state == 'u':
            self.state = 'g'
            self.changeState('Good')
        elif self.state == 'g':
            self.state = 'f'
            self.changeState('Fair')

        elif self.state == 'f':
            self.state = 's'
            self.changeState('Serious')

        elif self.state == 's':
            self.state = 'u'
            self.changeState('Undetermined')

    def changeState(self, state):
        self.env['hms.logs'].create({
            'details': "Patient State Changed To " + state,
            'patient_id': self.id
        })

    @api.model
    def create(self, val):
        new_patient = super().create(val)
        return new_patient

    @api.onchange('department_id')
    def onchange_department_id(self):
        if not self.department_open and self.first_name:
            raise exceptions.UserError("This Department is closed.")

    @api.onchange('age')
    def onchange_age(self):
        if self.first_name and self.age < 30:
            self.pcr = True
            return {
                'warning': {'title': 'take attention', 'message': 'The PCR option has been checked because age > 30.'}}


    @api.constrains("email")
    def check_valid_email(self):
        for record in self :
            if re.match('[a-z0-9]+@[a-z]+\.[a-z]{2,3}',record.email) == None:
                raise UserError("Enter Valid Email")

    _sql_constraints=[
        ('Duplicate_Email','UNIQUE(email)','Email is already exists, Try another one please.center()')
    ]

    @api.depends("birth_date")
    def _calc_age(self):
        for record in self:
            today = date.today()
            if record.birth_date is not False:
                record.age = (datetime.today().date() - datetime.strptime(str(record.birth_date),'%Y-%m-%d').date())
            else:
                record.age=0

    @api.onchange("age")
    def onchange_age(self):
        self.pcr=False
        if self.age<30:
            self.pcr=True
            return {
                "warning":{
                    "title":"PCR Message",
                    "message":"PCR has been checked."
                }
            }
