from odoo import api, fields, models, _


class MyMaintenanceActivityType(models.Model):
    _name = "my.maintenance.activity.type"
    _description = "Activity Type"

    name = fields.Char(string='Name', required=True)
    category = fields.Selection([
        ('none', 'None'),
        ('upload_document', 'Upload Document'),
        ('phonecall', 'Phonecall'),
        ('meeting', 'Meeting'),
    ], default=None)
    default_user_id = fields.Many2one('res.users', string='Default User')
