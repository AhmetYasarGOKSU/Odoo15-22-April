from odoo import api, fields, models, _


class Maintenance(models.Model):
    _name = "maintenance"
    _description = "Maintenance"

    name = fields.Char(string='Request', required=True)
    # equipment_list = fields.Many2one('equipments', string='Equipment')
    # request_date = fields.Date(string='Request Date')
