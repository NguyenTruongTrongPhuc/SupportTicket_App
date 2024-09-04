from odoo import fields, models, api

class TicketResponse(models.Model):
    _name = 'support.ticket.response'
    _description = 'Support Ticket Status'
    
    name = fields.Char(string = "Name", required = True)
    color = fields.Integer(string = "Color")