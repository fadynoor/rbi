from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    attachment = fields.Binary('Receipt', attachment=True)
    attachment_filename = fields.Char('Filename')
    attachment_date = fields.Date('Upload Date')