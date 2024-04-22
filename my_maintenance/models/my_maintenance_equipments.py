from odoo import api, fields, models, _


class Equipments(models.Model):
    _name = 'equipments'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Equipments'

    name = fields.Char(string='Equipment Name', required=True, tracking=True)
    equipment_category_id = fields.Many2one('equipment.categories', string='Equipment Category')
    owner_id = fields.Many2one('res.users', string='Owner')
    maintenance_team_id = fields.Many2one('maintenance.teams', string='Maintenance Team')
    assigned_date = fields.Date(string='Assigned Date')
    used_in_location = fields.Char(string='Used in location')
    scrap_date = fields.Date(string='Scrap Date')
    technician_id = fields.Many2one('res.users', string='Technician')
    description_note = fields.Text(string="Description")
    vendor = fields.Many2one('res.partner', string='Vendor')
    vendor_reference = fields.Char(string='Vendor Reference')
    model = fields.Char(string='Model')
    serial_number = fields.Char(string='Serial Number')
    effective_date = fields.Date(string='Effective Date', required=True)
    cost = fields.Float(string='Cost')
    warranty_expiration_date = fields.Date(string='Warranty Expiration Date')
    preventive_maintenance_frequency = fields.Integer(string='Preventive Maintenance Frequency')
    maintenance_duration = fields.Float(string='Maintenance Duration')
    maintenance_count = fields.Integer(string='Maintenance', compute='_compute_maintenance_count')
    # equipment_count = fields.Integer(string='Equipment Count', compute='_compute_equipment_count')


    @api.onchange('equipment_category_id')
    def onchange_equipment_category_id(self):
        if self.equipment_category_id:
            if self.equipment_category_id.name:
                self.name = self.equipment_category_id.name
        else:
            self.name = ''

    @api.onchange('maintenance_team_id')
    def onchange_maintenance_team_id(self):
        if self.maintenance_team_id:
            if self.maintenance_team_id.name:
                self.name = self.maintenance_team_id.name
        else:
            self.name = ''

    # def _compute_maintenance_count(self):
    #     for rec in self:
    #         maintenance_count = self.env['equipments'].search_count([('patient_id', '=', rec.id)])
    #         rec.appointment_count = maintenance_count

    # def _compute_equipment_count(self):
    #     for rec in self:
    #         equipment_count = self.env['equipment'].search_count([('equipments_id', '=', rec.id)])
    #         rec.equipment_count = equipment_count
