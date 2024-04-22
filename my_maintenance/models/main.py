from odoo import api, fields, models, _


class MyMaintenance(models.Model):
    _name = "my.maintenance"
    _description = "My Maintenance"

    name = fields.Char(string='name', required=True)
