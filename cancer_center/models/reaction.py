from odoo import models, fields

class Reaction(models.Model):
    _name = "cancer_center.reaction"
    _description = "Chemotherapy reaction"

    cure_id = fields.Many2one('cancer_center.cure', string='cure')
    degre = fields.Integer('degree')
    comment = fields.Text('comment')



