from odoo import api, fields, models, _


class MyMaintenanceTeam(models.Model):
    _name = "my.maintenance.team"
    _description = "Maintenance Team"

    name = fields.Char('Team Name', required=True, tracking=True)
    color = fields.Integer('Color Index')
    member_ids = fields.Many2many('res.users', string='Team Members', tracking=True)
