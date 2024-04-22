from odoo import api, fields, models, _


class MaintenanceTeams(models.Model):
    _name = "maintenance.teams"
    _description = "Maintenance Teams"

    name = fields.Char('Team Name', required=True, tracking=True)
    teams_id = fields.Many2many('res.users', string='Team Members', tracking=True)
