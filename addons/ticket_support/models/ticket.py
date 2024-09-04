from odoo import fields, models, api  # type: ignore
from datetime import datetime, timedelta

class Ticket(models.Model):
    _name = 'support.ticket'
    _description = 'Support Ticket'
    _rec_name = 'ticket_code'

    is_customer = fields.Boolean(string="Is Customer", default = True)
    # name = fields.Char(string = "Name", required = True)
    
    ################################
    #                              #
    #      Basic information       #                
    #                              #
    ################################
    ticket_code = fields.Char(string="Ticket Code",
                              readonly=True,
                              #computed="_compute_ticket_code",
                              store=True,
                              help="Ticket Code"
                              )
    name = fields.Char(string="Ticker Title",
                               required=True,
                               help="Ticket Title"
                               )
    custom_create_date = fields.Datetime(string="Create Day")
    nearest_response_date = fields.Datetime(string="Response Day")
    stage = fields.Many2one('support.ticket.stage',
                            string="Ticket Stage",
                            readonly = True,
                            group_expand="_read_group_stage"  # for getting all the stage
                            )
    content = fields.Html(string="Ticket description", help="Description")

    status = fields.Many2one('support.ticket.status', string="Status", readonly = True)

    ticket_response = fields.One2many('support.ticket', 'parent_ticket_id', string="Ticket Response")
    note = fields.Text(string="Note")
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], default='new', string="State")

    # internal user
    user = fields.Many2many('res.users', string="User")
    user_image = fields.Binary(related='user.image_1920', string='User Image')

    ####################
    #                  #
    #     customer     #
    #                  #
    ####################
    customer_id = fields.Many2one('res.partner', string="Customer")
    email = fields.Char(string="Email", related="customer_id.email")
    phone = fields.Char(string="Phone", related="customer_id.phone")
    website = fields.Char(string="Website", related="customer_id.website")

    # Added Many2one field to establish the inverse relation
    parent_ticket_id = fields.Many2one('support.ticket', string="Parent Ticket")
    ticket_type = fields.Selection([
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3'),
    ], string="Ticket Type")
    
    @api.model
    def _read_group_stage(self, group, domain,order):
        return self.env['support.ticket.status'].search([])


    def action_send_email(self):
        mail_template = self.env.ref('real-estate-ads.offer_mail_template')
        mail_template.send_mail(self.id, force_send=True)

    # @api.depends('id')
    # def _compute_ticket_code(self):
    #     pass
    
    @api.onchange('stage')
    def _onchange_stage(self):
        if self.stage:
            self.status = self.stage.status

    # def action_new(self):
    #     self.state = 'new'
        
    # def action_in_progress(self):
    #     self.state = 'in_progress'
        
    # def action_done(self):
    #     self.state = 'done'
        
    # status_class = fields.Char(compute='_compute_status_class', string="Status Class")
    
    color = fields.Integer(string="Color", compute = "update_ticket_status_color")

    @api.model
    def update_ticket_status_color(self):
        today = fields.Datetime.now()
        tickets = self.env['support.ticket'].search([])
        for ticket in tickets:
            if ticket.custom_create_date:
                valid_days = (today - ticket.custom_create_date).days
                if valid_days < 1:
                    ticket.color = 10 # Green
                elif 1 <= valid_days <= 7:
                    ticket.color = 3 # Yellow
                else:
                    ticket.color = 1 # Red
            else:
                ticket.color = 0
                
    # def write(self, vals):
    #     if 'stage_id' in vals:
    #         stage = self.env['support.ticket.stage'].browse(vals['stage_id'])
    #         if stage.status_id:
    #             vals['status'] = stage.status_id.id
    #     return super(Ticket, self).write(vals)
    

                
    boolean_toggle = fields.Boolean(string="User Mode", default=False)

    
    
