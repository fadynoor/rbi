from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    is_dp_invoice = fields.Boolean('Is DP', compute='_is_dp_invoice', store=True)
    
    @api.depends('invoice_line_ids')
    def _is_dp_invoice(self):
        for invoice in self:
            if invoice.type != 'out_invoice':
                invoice.is_dp_invoice = False
            else:
                dp_product_id = self.env['ir.config_parameter'].sudo().get_param('sale.default_deposit_product_id', False)
                if all(
                    [product_id == int(dp_product_id) for product_id in invoice.invoice_line_ids.product_id.ids]
                    ):
                    invoice.is_dp_invoice = True

    @api.model
    def create(self, vals):
        invoice = super(AccountMove, self).create(vals)
        invoice.activity_update()
        return invoice

    def action_post(self):
        invoice = super(AccountMove, self).action_post()
        self.activity_update()
        return invoice

    def button_cancel(self):
        invoice = super(AccountMove, self).button_cancel()
        self.activity_update()
        return invoice

    def button_draft(self):
        invoice = super(AccountMove, self).button_draft()
        self.activity_update()
        return invoice
    
    # TODO: blocking attach bila invoice DP statusnya belum post

    # auto hapus activity bila lebih dari date_deadline
    # supaya activity gak numpuk di notif admin
    def delete_late_activities(self, date=False, delay=False):
        invoices = self.env['account.move'].search([('type','=', 'out_invoice')])
        activities = invoices.mapped('activity_ids')
        date_end = date.strftime('%Y-%m-%d') if date else fields.Date.today()
        date_end = date_end - timedelta(days=delay or 1)
        activities.filtered(lambda act: act.date_deadline < date_end).unlink()
        

    def activity_update(self):
        for invoice in self.filtered(lambda inv: inv.type == 'out_invoice' and inv.state == 'draft'):
            activity_type = self.env.ref('account_rbi.mail_activity_invoice_post')
            activity_vals = {
                'activity_type_id': activity_type.id,
                'date_deadline': datetime.now() + timedelta(days=activity_type.delay_count)
            }
            self.activity_schedule(summary='Post Invoice', **activity_vals)
        
        for invoice in self.filtered(lambda inv: inv.type == 'out_invoice' and inv.state == 'posted'):
            self.activity_feedback(['account_rbi.mail_activity_invoice_post'])
            
            customer = invoice.sudo().partner_id
            user = customer.user_ids
            if not user:
                user = customer.parent_id.user_ids

            if invoice.message_attachment_count == 0:
                activity_type = self.env.ref('account_rbi.mail_activity_invoice_receipt')
                activity_vals = {
                    'activity_type_id': activity_type.id,
                    'user_id': user.id,
                    'date_deadline': datetime.now() + timedelta(days=activity_type.delay_count)
                }
                self.activity_schedule(summary='Attach Payment Receipt', **activity_vals)
            # TODO: find how to trigger paid invoice
            # elif invoice.invoice_payment_state == 'paid':
            #     self.activity_feedback(['account_rbi.mail_activity_invoice_paid'])
            else:
                self.activity_feedback(['account_rbi.mail_activity_invoice_receipt'])
                activity_type = self.env.ref('account_rbi.mail_activity_invoice_paid')
                activity_vals = {
                    'activity_type_id': activity_type.id,
                    'date_deadline': datetime.now() + timedelta(days=activity_type.delay_count)
                }
                self.activity_schedule(summary='Register Payment', **activity_vals)
            
        for invoice in self.filtered(lambda inv: inv.type == 'out_invoice' and inv.state == 'cancel'):     
            self.activity_unlink(['account_rbi.mail_activity_invoice_post'])
            self.activity_unlink(['account_rbi.mail_activity_invoice_receipt'])
            self.activity_unlink(['account_rbi.mail_activity_invoice_paid'])


    