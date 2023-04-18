from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    surviving_ticket = fields.Many2one(comodel_name="helpdesk.ticket", string="Surviving_ticket", ondelete="cascade", index=True,)
    archived_tickets = fields.One2many(comodel_name="helpdesk.ticket", inverse_name="surviving_ticket", string="Archived Tickets", context={'active_test': False}, readonly=True)

    def _action_open_merge_tickets(self):
        active_tickets = self.env['helpdesk.ticket'].browse(self._context.get('active_ids', []))
        return {
            'name': 'Merge Tickets',
            'view_mode': 'form',
            'res_model': 'merge.ticket',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('TicketMerge.merge_ticket_view_form').id,
            'target': 'new',
            'context': {
                'partner_ids': active_tickets.mapped('partner_id.id'),
                'user_ids': active_tickets.mapped('user_id.id'),
            }
        }
