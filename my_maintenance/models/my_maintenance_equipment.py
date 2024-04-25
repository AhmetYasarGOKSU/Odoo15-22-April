from odoo import api, fields, models, _
from datetime import datetime


class MyMaintenanceEquipment(models.Model):
    _name = "my.maintenance.equipment"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Maintenance Equipment"

    vendor = fields.Many2one('res.partner', string='Vendor')
    owner_id = fields.Many2one('res.users', string='Owner')
    maintenance_team_id = fields.Many2one('my.maintenance.team', string='Maintenance Team')
    equipment_category_id = fields.Many2one('my.maintenance.equipment.category', string='Equipment Category')
    technician_id = fields.Many2one('res.users', string='Technician')
    responsible_id = fields.Many2one('res.users', string='Responsible', tracking=True)
    used_by = fields.Selection([('department', 'Department'),
                                ('employee', 'Employee'),
                                ('other', 'Other')], default='employee')
    department_id = fields.Many2one('hr.department', string='Department')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    serial_number = fields.Char('Serial Number', copy=False)
    color = fields.Integer('Color Index')
    name = fields.Char(string='Equipment Name', required=True, tracking=True)
    used_in_location = fields.Char(string='Used in location')
    description_note = fields.Html(string="Description")
    vendor_reference = fields.Char(string='Vendor Reference')
    model = fields.Char(string='Model')
    cost = fields.Float(string='Cost')
    preventive_maintenance_frequency = fields.Integer(string='Preventive Maintenance Frequency')
    maintenance_duration = fields.Float(string='Maintenance Duration')
    maintenance_count = fields.Integer(string='Maintenance', compute='_compute_maintenance_count')
    scrap_date = fields.Date(string='Scrap Date')
    warranty_expiration_date = fields.Date(string='Warranty Expiration Date')
    assigned_date = fields.Date(string='Assigned Date', default=datetime.today())
    effective_date = fields.Date(string='Effective Date', required=True, default=datetime.today())

    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))

    @api.onchange('equipment_category_id')
    def onchange_equipment_category_id(self):
        if self.equipment_category_id:
            if self.equipment_category_id.name:
                self.technician_id = self.equipment_category_id.responsible_id
        else:
            self.name = ''

    @api.model
    def create(self, vals):
        global res
        if vals['equipment_category_id'] == 1:
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('seq_computers') or _('New')
            res = super(MyMaintenanceEquipment, self).create(vals)

        elif vals['equipment_category_id'] == 2:
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('seq_software') or _('New')
            res = super(MyMaintenanceEquipment, self).create(vals)

        elif vals['equipment_category_id'] == 3:
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('seq_printers') or _('New')
            res = super(MyMaintenanceEquipment, self).create(vals)

        elif vals['equipment_category_id'] == 4:
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('seq_monitors') or _('New')
            res = super(MyMaintenanceEquipment, self).create(vals)

        elif vals['equipment_category_id'] == 5:
            if vals.get('reference', _('New')) == _('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('seq_phones') or _('New')
            res = super(MyMaintenanceEquipment, self).create(vals)
        return res

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

