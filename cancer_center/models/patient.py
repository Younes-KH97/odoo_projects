from odoo import models, fields

class Patient(models.Model):
    _name = "cancer_center.patient"
    name = fields.Char()
    dob = fields.Date()
    address_of_residence = fields.Char() # Make a Select from a json of wilayas
    phone_number = fields.Char("phone number")

    # protocols_ids = fields.Many2many('cancer_center.protocol', string='protocols')
    protocol_assignment_ids = fields.One2many('cancer_center.protocol.assignment', 'patient_id', string='protocol_assignment')

    def action_open_program_form(self):
        return {
            'name': 'Assign Program',
            'type': 'ir.actions.act_window',
            'res_model': 'cancer_center.protocol.assignment',
            'view_mode': 'form',
            'target': 'new',  # shows in side popup
            'context': {
                'default_patient_id': self.id
            }
        }
