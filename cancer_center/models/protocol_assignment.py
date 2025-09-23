from odoo import models, fields, api
from datetime import timedelta, datetime

class ProtocolAssignment(models.Model):
    _name = "cancer_center.protocol.assignment"
    _description = "Chemotherapy protocol assignment"

    patient_id = fields.Many2one('cancer_center.patient', string='patient')
    protocol_id = fields.Many2one('cancer_center.protocol', string='protocol')
    protocol_assignment_detail_ids = fields.One2many('cancer_center.protocol.assignment.detail', 
                                             'protocol_assignment_id', 
                                              string='prot assig detail')
    cure_ids = fields.One2many('cancer_center.cure', 'protocol_assignment_id', string='cures')
    

    date_start = fields.Date(string="Start Date", required=True)
    interval = fields.Integer('interval')
    number_of_cures = fields.Integer('number_of_cures')
    

    @api.model_create_multi
    def create(self, vals):
        prot_assig_record = super().create(vals)
        for val in vals:
            interval = val["interval"]
            date_start = val["date_start"]
            curr_date = datetime.strptime(date_start, '%Y-%m-%d').date()
            number_of_cures = val["number_of_cures"]
            for i in range(number_of_cures):
                for index,protocol_detail in enumerate(val['protocol_assignment_detail_ids']):
                    if index > 0: 
                        curr_date = curr_date + timedelta(days=protocol_detail[2]["day_number"])
                    self.env["cancer_center.cure"].create({
                        "medication_id": protocol_detail[2]["medication_id"],
                        "weight": 0.0,
                        "date_of_cure": curr_date,
                        "protocol_assignment_id": prot_assig_record.id
                    })
                curr_date = curr_date + timedelta(days=interval)
        return prot_assig_record


    def show_planning(self):
        self.ensure_one()
        return {
            'name': 'All program',
            'type': 'ir.actions.act_window',
            'res_model': 'cancer_center.cure',
            'view_mode': 'tree',
            'target': 'main',  # shows in side popup
            'domain': [('protocol_assignment_id', '=', self.id)],
            'context': {
                'default_protocol_assignment_id': self.id
            }
        }