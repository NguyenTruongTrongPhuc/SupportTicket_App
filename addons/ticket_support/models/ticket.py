from odoo import fields, models, api  # type: ignore
import logging
from datetime import datetime, timedelta

class Ticket(models.Model):
    _name = 'support.ticket'
    _description = 'Support Ticket'
    _rec_name = 'ticket_code'

    is_customer = fields.Boolean(string="Is Customer", default = False)
    # partner issue the ticket
    # both user and partner can issue the ticket (and both can be shown as res.partner)
    partner_issue_ticket = fields.Many2one('res.partner', string="Customer")

    ################################
    #                              #
    #      Basic information       #                
    #                              #
    ################################
    ticket_code = fields.Char(string="Ticket Code",
                              readonly=True,
                              compute="_compute_ticket_code",
                              store = True,
                              help="Ticket Code"
                              )
    name = fields.Char(string="Ticker Title",
                       required=True,
                       help="Ticket Title"
                       )
    custom_create_date = fields.Datetime(string="Create Day", default=fields.Datetime.now)

    stage = fields.Many2one('support.ticket.stage',
                            string="Ticket Stage",
                            group_expand="_read_group_stage"  # for getting all the stage
                            )
    # left side is the value, right side is the string that is shown
    # we can utilizing the left size to store the color code
    status = fields.Selection([
        ("10", "New"),
        ("3", "In Week"),
        ("1", "In Month"),
        ],
        string="Status")

    content = fields.Html(string="Ticket description", help="Description")

    ticket_additional = fields.One2many('support.ticket', 'parent_ticket_id', string="Ticket Response")

    note = fields.Html(string="Note")

    # inhouse user to handle the ticket
    user_handling = fields.Many2many('res.users', string="User")
    user_handling_image = fields.Binary(related='user_handling.image_1920', string='User Image')

    ####################
    #                  #
    #     customer     #
    #                  #
    ####################
    email = fields.Char(string="Email", related="partner_issue_ticket.email")
    phone = fields.Char(string="Phone", related="partner_issue_ticket.phone")
    website = fields.Char(string="Website", related="partner_issue_ticket.website")

    # Added Many2one field to establish the inverse relation
    parent_ticket_id = fields.Many2one('support.ticket', string="Parent Ticket")

    ticket_type = fields.Many2one('support.ticket.type', string="Ticket Type")

    
    # @api.model
    # def create(self,vals):
    #     res = super(Ticket, self).create(vals)
    #     res.update_status()
    #     res.compute_color()
    
    
    @api.model
    def _read_group_stage(self, group, domain, order):
        return self.env['support.ticket.stage'].search([])
    
    color = fields.Integer(string="Color", compute="compute_color")

    @api.model
    def update_status(self):
        datetime_now = datetime.now()
        for ticket in self.search([]):
            if ticket.custom_create_date:
                create_date = fields.Datetime.from_string(ticket.custom_create_date)
                if (datetime_now - create_date).days <= 1:
                    ticket.status = "10"
                elif(datetime_now - create_date).days <= 7:
                    ticket.status = "3"
                else:
                    ticket.status = "1"
                ticket.compute_color()

    @api.depends("status")
    def compute_color(self):
        for rec in self:
            if rec.status:
                rec.color = int(rec.status)
            else:
                rec.color = 0


    def _compute_ticket_code(self):
        for ticket in self:
            ticket.ticket_code = "TK" + str(ticket.id).zfill(10)           
