from odoo import models, fields

class TicketStage(models.Model):
    _name = 'support.ticket.stage'
    _description = 'Stage'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string = "Color")