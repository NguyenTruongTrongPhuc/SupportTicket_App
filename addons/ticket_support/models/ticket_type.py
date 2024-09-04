from odoo import fields, models, api

class TicketType(models.Model):
    _name = 'support.ticket.type'
    _description = 'Support Ticket Type'
    
    name = fields.Char(string = "Name", required = True)
    color = fields.Char(string = "Color")