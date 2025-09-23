from odoo import models, fields

class Protocol(models.Model):
    _name = "cancer_center.protocol"
    _description = "Chemotherapy protocol"

    patients_ids = fields.Many2many('cancer_center.patient', string='patients')
    name = fields.Char()



