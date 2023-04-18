{
    'name': 'Helpdesk Ticket Merger',
    'version': '1.0',
    'category': 'Helpdesk',
    'summary': 'Merge multiple helpdesk tickets',
    'author': 'Simplify-ERP™',
    'website': 'https://simplify-erp.de',
    'depends': ['helpdesk', 'helpdesk_timesheet'],
    'data': [
        'views/helpdesk_ticket.xml',
        'wizard/merge_ticket.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
