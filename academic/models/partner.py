from odoo import models, fields, api

class Partnet(models.Model):
    _inherit = 'res.partner'

    is_instructor = fields.Boolean(string="Instructor", default=False,)
    session_ids = fields.Many2many("academic.session", string="Attended sessions", readonly=True,)
