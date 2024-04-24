from odoo import api, fields, models, _
from datetime import datetime


class MyMaintenanceEquipment(models.Model):
    _name = 'my.maintenance.equipment'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'My Maintenance Equipment'

    name = fields.Char(string='Equipment Name', required=True, tracking=True)
    equipment_category_id = fields.Many2one('my.maintenance.equipment.category', string='Equipment Category')
    equipment_category_name = fields.Char(related='equipment_category_id.name')
    owner_id = fields.Many2one('res.users', string='Owner')
    maintenance_team_id = fields.Many2one('my.maintenance.team', string='Maintenance Team')
    assigned_date = fields.Date(string='Assigned Date', default=datetime.today())
    used_in_location = fields.Char(string='Used in location')
    scrap_date = fields.Date(string='Scrap Date')
    technician_id = fields.Many2one('res.users', string='Technician')
    description_note = fields.Text(string="Description")
    vendor = fields.Many2one('res.partner', string='Vendor')
    vendor_reference = fields.Char(string='Vendor Reference')
    model = fields.Char(string='Model')
    serial_number = fields.Char(string='Serial Number')
    effective_date = fields.Date(string='Effective Date', default=datetime.today(), required=True)
    cost = fields.Float(string='Cost')
    warranty_expiration_date = fields.Date(string='Warranty Expiration Date')
    preventive_maintenance_frequency = fields.Integer(string='Preventive Maintenance Frequency')
    maintenance_duration = fields.Float(string='Maintenance Duration')
    maintenance_count = fields.Integer(string='Maintenance', compute='_compute_maintenance_count')
    reference = fields.Char(string='Order Reference', required=True, readonly=True, copy=False,
                            default=lambda self: _('New'))

    @api.onchange('equipment_category_id')
    def onchange_equipment_category_id(self):
        if self.equipment_category_id:
            if self.equipment_category_id.name:
                self.technician_id = self.equipment_category_id.responsible_id
        else:
            self.name = ''

    def _compute_maintenance_count(self):
        for rec in self:
            maintenance_count = self.env['my.maintenance.equipment'].search_count([('equipment_category_id', '=', rec.id)])
            rec.maintenance_count = maintenance_count

    def action_open_maintenance(self):
        return {
            "type": "ir.actions.act_window",
            "name": 'Equipment',
            "res_model": "my.maintenance.equipment",
            "domain": [('equipment_category_id', '=', self.id)],
            "view_mode": 'tree,form',
            "target": 'current',
        }

    @api.model
    def create(self, vals):
        if vals['equipment_category_id'] == 1:
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code("seq_computers") or _("New")
            res = super(MyMaintenanceEquipment, self).create(vals)
            return res

    # @api.model
    # def create(self, vals):
    #     print(vals['equipment_category_id'])
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code("seq_computers") or _("New")
    #     res = super(MyMaintenanceEquipment, self).create(vals)
    #     return res
