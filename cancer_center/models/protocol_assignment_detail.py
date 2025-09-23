from odoo import models, fields

class ProtocolAssignmentDetail(models.Model):
    _name = "cancer_center.protocol.assignment.detail"
    _description = "Protocol assignment details"

    protocol_assignment_id = fields.Many2one('cancer_center.protocol.assignment', 
                                             string='protocol_assignment_detail')

    day_number = fields.Integer('day_number')
    medication_id = fields.Many2one('cancer_center.medication', 
                                    string='medication_id')

