from odoo import models, fields, api

class CureStatistics(models.Model):
    _name = "cancer_center.cure.statistics"
    _description = "Chemotherapy cure statistics"

    total_today_cures = fields.Integer( string='total_today_cures')
    total_week_cures = fields.Integer( string='total_week_cures')
    total_month_cures = fields.Integer( string='total_month_cures')
    total_year_cures = fields.Integer( string='total_year_cures')
    
