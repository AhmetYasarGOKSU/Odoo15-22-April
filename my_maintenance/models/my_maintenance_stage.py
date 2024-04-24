from odoo import api, fields, models, _


class MyMaintenanceStage(models.Model):
    _name = "my.maintenance.stage"
    _description = "Maintenance Stage"
    _order = "sequence, id"

    name = fields.Char(string='Name', required=True)
    fold = fields.Boolean(string='Folded in Maintenance Pipe')
    done = fields.Boolean(string='Request Done')
    sequence = fields.Integer(string='Sequence', default=1)

    # @api.model
    # def create(self, vals):
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code("my.maintenance.stage") or _("New")
    #     res = super(MyMaintenanceStage, self).create(vals)
    #     return res
