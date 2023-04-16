from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    def action_merge_tickets(self, ticket_ids):
        # Get the tickets to merge
        tickets = self.browse(ticket_ids)

        # Find the oldest ticket
        surviving_ticket = min(tickets, key=lambda t: t.create_date)

        # Merge titles and descriptions
        surviving_ticket.title = ' '.join(tickets.mapped('title'))
        surviving_ticket.description = ' '.join(tickets.mapped('description'))

        # Merge timesheets and time estimations
        for ticket in tickets - surviving_ticket:
            ticket.timesheet_ids.write({'ticket_id': surviving_ticket.id})
            surviving_ticket.planned_hours += ticket.planned_hours

            # Add a link to the archived ticket in the description
            surviving_ticket.description += f'\n\n[Archived Ticket {ticket.id}]({ticket.get_portal_url()})'

            # Archive the ticket
            ticket.active = False

        return surviving_ticket
