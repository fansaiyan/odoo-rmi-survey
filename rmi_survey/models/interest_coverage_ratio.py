from odoo import models, fields, api

class InterestCoverageRatio(models.Model):
    _name = 'rmi.icr'
    _description = 'Interest Coverage Ratio'

    name = fields.Char(string='Peringkat', required=True)
    min = fields.Float(string='Min', required=True)
    max = fields.Float(string='Max', required=True)