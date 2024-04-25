from odoo import api, fields, models, _


class MyMaintenanceMain(models.Model):
    _name = "my.maintenance.main"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "My Maintenance Main"

    name = fields.Char(string='name', required=True)
