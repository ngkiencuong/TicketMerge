from odoo import fields, models, _
from odoo.exceptions import ValidationError


class MergeTickets(models.TransientModel):
    _name = 'merge.ticket'
    _description = "Merge tickets wizard"

    def _domain_partner_id(self):
        partner_ids = self._context.get('partner_ids', False)
        return [('id', 'in', partner_ids)] if partner_ids else []

    def _domain_user_id(self):
        user_ids = self._context.get('user_ids', False)
        return [('id', 'in', user_ids)] if user_ids else []

    partner_id = fields.Many2one('res.partner', string='Customer', domain=_domain_partner_id, help='You can only merge tickets from the same customer')
    user_id = fields.Many2one('res.users', string='Assigned to', domain=_domain_user_id, help='This will be the assignee for the surviving ticket')

    def merge_ticket(self):
        # Get the tickets to merge
        tickets = self.env['helpdesk.ticket'].browse(self._context.get('active_ids', []))
        # Find the oldest ticket
        surviving_ticket = min(tickets, key=lambda t: t.create_date)
        # Merge titles, descriptions, assignee and customer
        surviving_ticket = surviving_ticket.sudo()
        surviving_ticket.name = ' '.join(tickets.mapped('name'))
        surviving_ticket.description = ' '.join(tickets.filtered_domain([('description', '!=', False)]).mapped('description'))
        surviving_ticket.user_id = self.user_id
        surviving_ticket.partner_id = self.partner_id
        # Merge timesheets
        for ticket in tickets - surviving_ticket:
            if ticket.timesheet_ids and not surviving_ticket.team_id.use_helpdesk_timesheet:
                raise ValidationError(_("Team in the surviving ticket doesn't allow timesheet. Please check it!"))
            ticket = ticket.sudo()
            ticket.timesheet_ids.write({'helpdesk_ticket_id': surviving_ticket.id})
            # Archive the ticket
            ticket.active = False
            # Add the link to the archived ticket
            ticket.surviving_ticket = surviving_ticket.id
            # merge chatter note and attachment
            for mess in self.env['mail.message'].search([('res_id', '=', ticket.id), ('model', '=', 'helpdesk.ticket')], order='id'):
                mess.sudo().write({'res_id': surviving_ticket.id})
            for attach in self.env['ir.attachment'].search([('res_id', '=', ticket.id), ('res_model', '=', 'helpdesk.ticket')]):
                attach.sudo().write({'res_id': surviving_ticket.id})
        return surviving_ticket
