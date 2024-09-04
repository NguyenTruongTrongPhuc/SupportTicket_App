{
    "name": "Support Ticket",
    "version": "1.0",
    "author": "phucnguyen12328",
    "description": """
     Technical Support Ticket module to show available properties
    """,
    "category": "Sales",
    "depends": ['base','web','mail'],
    "data": [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'security/res_groups.xml',
        'security/model_access.xml',
                  
        'views/ticket_view.xml',
        'views/ticket_type_view.xml',
        'views/ticket_status_view.xml',
        'views/ticket_response_view.xml',
        'views/menu_items.xml',
    ],
    "installable" : True,
    "application" : True,
    "license" : "LGPL-3",
    'auto_install': False,
}