from odoo import api, fields, models, _
from datetime import datetime


class MyMaintenanceRequest(models.Model):
    _name = "my.maintenance.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "My Maintenance Request"

    name = fields.Char(string="Request", required=True)
    email_cc = fields.Char('Email cc', help='List of cc from incoming emails.')
    req_date = fields.Date(string='Request Date', readonly=True, default=datetime.today())
    color = fields.Integer('Color Index')
    active = fields.Boolean(default=True)
    duration = fields.Float(string='Duration')
    schedule_date = fields.Datetime(string='Scheduled Date')

    maintenance_team_id = fields.Many2one('my.maintenance.team', string='Team')
    owner_user_id = fields.Many2one('res.users', string='Owner', tracking=True)
    category_id = fields.Many2one('my.maintenance.equipment.category', string='Category')
    partner_id = fields.Many2one('res.partner', string='Vendor', check_company=True)
    user_id = fields.Many2one('res.users', string='Responsible')
    equipment_id = fields.Many2one('my.maintenance.equipment', string='Equipment')
    description = fields.Html(string='Description')

    priority = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High')], string='Priority')

    maintenance_type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive')],
                                        string='Maintenance Type', default="corrective")
    # State
    state = fields.Selection([('new_request', 'New Request'), ('in_progress', 'In Progress'),
                              ('repaired', 'Repaired'), ('scrap', 'Scrap'), ('cancel', 'Cancel')], default='new_request',
                             string="Status", tracking=True)

    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    string='Kanban State', required=True, default='normal', tracking=True)

    # type_of_transfer field onchange -> make status to false
    @api.onchange('type_of_transfer')
    def _onchange_type_of_transfer(self):
        if self.type_of_transfer == 'internal':
            self.outside = False
        elif self.type_of_transfer == 'external':
            self.inside = False

    @api.onchange('equipment_id')
    def onchange_equipment_id(self):
        if self.equipment_id:
            self.user_id = self.equipment_id.technician_user_id if self.equipment_id.technician_user_id else self.equipment_id.category_id.technician_user_id
            self.category_id = self.equipment_id.category_id
            if self.equipment_id.maintenance_team_id:
                self.maintenance_team_id = self.equipment_id.maintenance_team_id.id

    # State
    def action_new_request(self):
        for rec in self:
            rec.state = 'new_request'

    def action_in_progress(self):
        for rec in self:
            rec.state = 'in_progress'

    def action_repaired(self):
        for rec in self:
            rec.state = 'repaired'

    def action_scrap(self):
        for rec in self:
            rec.state = 'scrap'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    # Onchange Function
    @api.onchange('equipment_id')
    # @api.onchange('patient_id', 'field_')
    def onchange_equipment_id(self):
        # is there value inside equipment_id?
        if self.equipment_id:
            # is there value inside equipment_id.name ?
            if self.equipment_id.name:
                # set value field name to user_id (to self.user_id)
                self.user_id = self.equipment_id.responsible_id