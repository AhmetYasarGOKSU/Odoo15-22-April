from odoo import api, fields, models, _


class MyMaintenanceEquipmentCategory(models.Model):
    _name = "my.maintenance.equipment.category"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Equipment Category"

    name = fields.Char(string='Category Name', required=True, tracking=True)
    responsible_id = fields.Many2one('res.users', string='Responsible', tracking=True, required=True)

    note = fields.Text(string='Comments', tracking=True)
    equipments = fields.Integer(string='Equipments')
    maintenance = fields.Integer(string='Maintenance')
    equipment_count = fields.Integer(string='Equipment Count', compute='_compute_equipment_count')
    maintenance_count = fields.Integer(string='Appointment Count', compute='_compute_maintenance_count')
    equipments_id = fields.Many2one('my.maintenance.equipment')

    def _compute_equipment_count(self):
        for rec in self:
            equipment_count = self.env['my.maintenance.equipment'].search_count([('equipment_category_id', '=', rec.id)])
            rec.equipment_count = equipment_count

    def _compute_maintenance_count(self):
        for rec in self:
            maintenance_count = self.env['my.maintenance.equipment'].search_count([('equipment_category_id', '=', rec.id)])
            rec.maintenance_count = maintenance_count

    @api.onchange('maintenance_team_id')
    def onchange_equipment_category_id(self):
        if self.equipments_id:
            if self.equipments_id.name:
                self.name = self.equipments_id.name
        else:
            self.name = ''

    def action_open_equipments_category(self):
        return {
            "type": "ir.actions.act_window",
            "name": 'Equipment',
            "res_model": "my.maintenance.equipment",
            "domain": [('equipment_category_id', '=', self.id)],
            "view_mode": 'tree,form',
            "target": 'current',
        }

    def action_open_maintenance(self):
        return {
            "type": "ir.actions.act_window",
            "name": 'Equipment',
            "res_model": "my.maintenance.equipment",
            "domain": [('equipment_category_id', '=', self.id)],
            "view_mode": 'tree,form',
            "target": 'current',
        }
