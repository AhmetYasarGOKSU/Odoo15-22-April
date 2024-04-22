from odoo import api, fields, models, _


class MaintenanceStages(models.Model):
    _name = "maintenance.stages"
    _description = "Maintenance Stages"
