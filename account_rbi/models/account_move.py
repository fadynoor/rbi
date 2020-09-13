from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    attachment = fields.Binary('Receipt', attachment=True)
    attachment_filename = fields.Char('Filename')
    attachment_date = fields.Date('Upload Date')

    # attachment_number = fields.Integer('Number of Attachments', compute='_compute_attachment_number')

    # def _compute_attachment_number(self):
    #     attachment_data = self.env['ir.attachment'].read_group([('res_model', '=', 'account.move'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
    #     attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
    #     for move in self:
    #         if move.type not in ['out_invoice', 'out_refund']:
    #             move.attachment_number = 0
    #         else:    
    #             move.attachment_number = attachment.get(move.id, 0)