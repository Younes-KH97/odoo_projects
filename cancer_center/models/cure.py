from odoo import models, fields, api
from datetime import timedelta
class Cure(models.Model):
    _name = "cancer_center.cure"
    _description = "Chemotherapy cure"

    protocol_assignment_id = fields.Many2one('cancer_center.protocol.assignment', 
                                             string='protocol_assignment')
    patient_id = fields.Many2one(
        'cancer_center.patient',
        string="Patient",
        related='protocol_assignment_id.patient_id',
        store=False  # optional: True if you want to sort/search
    )

    reaction_ids = fields.One2many('cancer_center.reaction', 'cure_id', string='reaction')
    height = fields.Float('height')
    weight = fields.Float('weight')
    note = fields.Text('note')
    date_of_cure = fields.Date('date_of_cure')
    medication_id = fields.Many2one('cancer_center.medication', string='medication')
    bsa = fields.Float('bsa', store=False)
    calculated_dose = fields.Float(compute='_compute_dose', store="True", string='dose')
    status_label = fields.Char(compute='_compute_status_label')
            
    
    @api.depends('calculated_dose', 'date_of_cure')
    def _compute_status_label(self):
        today = fields.Date.today()
        for rec in self:
            if rec.calculated_dose > 0 and rec.reaction_ids:
                rec.status_label = 'Réaction'
            elif rec.calculated_dose > 0:
                rec.status_label = 'Injectée'
            elif rec.date_of_cure == today:
                rec.status_label = 'Aujourd\'hui'
            else:
                rec.status_label = 'En attente'
    
    @api.depends('weight', 'height', 'medication_id')
    def _compute_dose(self):
        for rec in self:
            if rec.weight and rec.height and rec.medication_id.posology:
                bsa = 0.007184 * (rec.weight ** 0.425) * (rec.height ** 0.725)
                rec.bsa = round(bsa, 3)
                rec.calculated_dose = round(bsa * rec.medication_id.posology, 2)

                today = fields.date.today()
                start_month = today.replace(day=1)
                start_year = today.replace(day=1, month=1)
                start_week = today - timedelta(days=today.weekday())

                cure_stats_model = self.env["cancer_center.cure.statistics"]
                stats_line = cure_stats_model.search([], limit=1)

                total_today_cures = self.search_count([('date_of_cure','=', today), 
                                                            ('calculated_dose','>','0')])
                total_week_cures = self.search_count([('date_of_cure','>=', start_week), 
                                    ('calculated_dose','>','0')])
                total_month_cures = self.search_count([('date_of_cure','>=', start_month), 
                                    ('calculated_dose','>','0')])
                total_year_cures = self.search_count([('date_of_cure','>=', start_year), 
                                    ('calculated_dose','>','0')]) 

                if not stats_line:
                    cure_stats_model.create({
                        "total_today_cures": total_today_cures,
                        "total_week_cures": total_week_cures,
                        "total_month_cures": total_month_cures,
                        "total_year_cures": total_year_cures         
                    })
                else:
                    stats_line.write({
                        "total_today_cures": total_today_cures,
                        "total_week_cures": total_week_cures,
                        "total_month_cures": total_month_cures,
                        "total_year_cures": total_year_cures})
            else:
                rec.bsa = 0.0
                rec.calculated_dose = 0.0

    def show_reactions(self):
        self.ensure_one()
        return {
            'name': 'All reactions',
            'type': 'ir.actions.act_window',
            'res_model': 'cancer_center.reaction',
            'view_mode': 'tree',
            'target': 'new',  # shows in side popup
            'domain': [('cure_id', '=', self.id)],
            'context': {
                'default_cure_id': self.id
            }
        }
    