from odoo import api, fields, models, _


class MyMaintenanceActivityType(models.Model):
    _name = "my.maintenance.activity.type"
    _description = "Activity Type"
    _order = "sequence, id"

    def _get_model_selection(self):
        return [
            (model.model, model.name)
            for model in self.env['ir.model'].sudo().search(
                ['&', ('is_mail_thread', '=', True), ('transient', '=', False)])
        ]

    name = fields.Char(required=True)
    sequence = fields.Integer(default=0)
    category = fields.Selection([
        ('none', 'None'),
        ('upload_file', 'Upload Document'),
        ('phonecall', 'Phonecall'),
        ('meeting', 'Meeting'),
    ], default='none', string='Action')

    default_user_id = fields.Many2one('res.users', string='Default User')
    res_model = fields.Selection(selection=_get_model_selection, string='Model')
    initial_res_model = fields.Selection(selection=_get_model_selection, string='Initial model',
                                         compute="_compute_initial_res_model", store=False,)
    res_model_change = fields.Boolean(string="Model has change" , default=False, store=False)

    @api.onchange('res_model')
    def _onchange_res_model(self):
        self.mail_template_ids = self.sudo().mail_template_ids.filtered(lambda template: template.model_id.model == self.res_model)
        self.res_model_change = self.initial_res_model and self.initial_res_model != self.res_model

    def _compute_initial_res_model(self):
        for activity_type in self:
            activity_type.initial_res_model = activity_type.res_model

    summary = fields.Char(string='Default Summary')
    icon = fields.Char(string='Icon')
    decoration_type = fields.Selection([
        ('warning', 'Alert'),
        ('danger', 'Error'),
    ])
    chaining_type = fields.Selection([
        ('suggest', 'Suggest Next Activity'),
        ('trigger', 'Trigger Next Activity'),
    ], default='suggest', string='Chaining Type', required=True)
    suggested_next_type_ids = fields.Many2many('my.maintenance.activity.type', 'maintenance_activity_rel'
                                               , 'recommended_id', 'activity_id', string='Suggest'
                                               , compute='_compute_suggested_next_type_ids',
                                               inverse='_inverse_suggested_next_type_ids')
    triggered_next_type_id = fields.Many2one('my.maintenance.activity.type', string='Trigger'
                                              , compute='_compute_triggered_next_type_id',
                                              inverse='_inverse_triggered_next_type_id')
    mail_template_ids = fields.Many2many('mail.template', string='Email templates')
    delay_count = fields.Integer(string='Schedule', default=0)
    delay_unit = fields.Selection([('days', 'days'),
                                   ('weeks', 'weeks'),
                                   ('months', 'months')], default='days', required=True)
    delay_from = fields.Selection([('current_date', 'after completion date'),
                                   ('previous activity', 'after previous activity deadline')],
                                  default='previous activity', required=True)
    default_note = fields.Html(string='Default Note')
    delay_label = fields.Char(compute='_compute_delay_label')

    @api.depends('delay_unit', 'delay_count')
    def _compute_delay_label(self):
        selection_description_values = {
            e[0]: e[1] for e in self._fields['delay_unit']._description_selection(self.env)}
        for activity_type in self:
            unit = selection_description_values[activity_type.delay_unit]
            activity_type.delay_label = '%s %s' % (activity_type.delay_count, unit)

    @api.depends('chaining_type')
    def _compute_suggested_next_type_ids(self):
        """suggested_next_type_ids and triggered_next_type_id should be mutually exclusive"""
        for activity_type in self:
            if activity_type.chaining_type == 'trigger':
                activity_type.suggested_next_type_ids = False

    def _inverse_suggested_next_type_ids(self):
        for activity_type in self:
            if activity_type.suggested_next_type_ids:
                activity_type.chaining_type = 'suggest'

    @api.depends('chaining_type')
    def _compute_triggered_next_type_id(self):
        """suggested_next_type_ids and triggered_next_type_id should be mutually exclusive"""
        for activity_type in self:
            if activity_type.chaining_type == 'suggest':
                activity_type.triggered_next_type_id = False

    def _inverse_triggered_next_type_id(self):
        for activity_type in self:
            if activity_type.triggered_next_type_id:
                activity_type.chaining_type = 'trigger'
            else:
                activity_type.chaining_type = 'suggest'
