from odoo import api, fields, models, _


class MyMaintenance(models.Model):
    _name = "my.maintenance"
    _description = "My Maintenance"

    name = fields.Char(string='Request', required=True)
    # equipment_list = fields.Many2one('equipments', string='Equipment')
    # request_date = fields.Date(string='Request Date')
