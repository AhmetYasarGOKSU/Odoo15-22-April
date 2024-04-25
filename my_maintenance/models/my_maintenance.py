from odoo import api, fields, models, _


class MyMaintenance(models.Model):
    _name = "my.maintenance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "My Maintenance"

    name = fields.Char(string='Request', required=True)

