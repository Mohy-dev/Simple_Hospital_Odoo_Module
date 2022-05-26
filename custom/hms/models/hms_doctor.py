from odoo import models, fields


class Doctor(models.Model):
    _name = "hms.doctor"
    
    first_name = fields.Text()
    last_name = fields.Text()
    image = fields.Image()
