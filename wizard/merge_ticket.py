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

    def action_confirm(self):
        tickets = self.env['helpdesk.ticket'].browse(self._context.get('active_ids', []))
        old_tickets = tickets.filtered(lambda x: x.archived_tickets)
        tickets = tickets + tickets.mapped('archived_tickets') - old_tickets
        new_ticket = self.merge_ticket(tickets)
        for rec in old_tickets:
            self.merge_chatter_attachment(rec, new_ticket)
            rec.timesheet_ids.sudo().write({'helpdesk_ticket_id': new_ticket.id})
        old_tickets.sudo().unlink()
        return new_ticket

    def merge_ticket(self, tickets):
        # Find the oldest ticket
        surviving_ticket = min(tickets, key=lambda t: t.create_date)
        new_ticket = surviving_ticket.copy(dict(active=True))
        for mess in self.env['mail.message'].search([('res_id', '=', new_ticket.id), ('model', '=', 'helpdesk.ticket')]):
            mess.sudo().unlink()
        # Merge titles, descriptions, assignee and customer
        new_ticket.name = ' '.join(tickets.mapped('name'))
        new_ticket.description = ' '.join(tickets.filtered_domain([('description', '!=', False)]).mapped('description'))
        new_ticket.user_id = self.user_id
        new_ticket.partner_id = self.partner_id
        # Merge timesheets
        for ticket in tickets:
            if ticket.timesheet_ids and not new_ticket.team_id.use_helpdesk_timesheet:
                raise ValidationError(_("Team in the surviving ticket doesn't allow timesheet. Please check it!"))
            ticket = ticket.sudo()
            ticket.timesheet_ids.write({'helpdesk_ticket_id': new_ticket.id})
            # Archive the ticket
            ticket.active = False
            # Add the link to the archived ticket
            ticket.surviving_ticket = new_ticket.id
            # merge chatter note and attachment
            self.merge_chatter_attachment(ticket, new_ticket)
        return new_ticket

    def merge_chatter_attachment(self, old_ticket, new_ticket):
        for mess in self.env['mail.message'].search([('res_id', '=', old_ticket.id), ('model', '=', 'helpdesk.ticket')]):
            mess.sudo().write({'res_id': new_ticket.id})
        for attach in self.env['ir.attachment'].search([('res_id', '=', old_ticket.id), ('res_model', '=', 'helpdesk.ticket')]):
            attach.sudo().write({'res_id': new_ticket.id})

