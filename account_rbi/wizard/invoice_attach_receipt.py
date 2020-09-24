from odoo import models, fields, api

import base64

class InvoiceAttachReceipt(models.TransientModel):
    _name = 'invoice.attach.wizard'
    _description = "Wizard: Attach Payment Receipt to Invoice"

    receipt = fields.Binary(string='Payment Receipt', required=True, attachment=False)
    receipt_name = fields.Char('Receipt Name')

    def attach_receipt(self):
        invoice_id = self._context.get('active_id')
        active_model = self._context.get('active_model')
        doc = self.env[active_model].browse(invoice_id)

        doc.sudo().message_post(body='Payment receipt attached', attachments=[(self.receipt_name, base64.decodebytes(self.receipt))])

        doc.sudo().activity_update()
