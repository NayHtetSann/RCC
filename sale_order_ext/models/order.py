from odoo import models, fields
from ..spreadsheet_api import Spreadsheet


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    attachment_id = fields.Binary('Attachment')
    file_name = fields.Char('File Name')
    path = fields.Char('Path')

    def redirect_url(self, redirect):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': f'/auth/signin?redirect={redirect}',
        }

    def preview_spreadsheet(self):
        self.ensure_one()
        baseUrl = self.env['ir.config_parameter'].sudo().get_param('18.base.url')
        username = self.env.user.use_login and self.env.user.login or self.env.user.username
        if self.path:
            return self.redirect_url(self.path)
        if not self.env.user.rpc_token:
            token = Spreadsheet.get_token(baseUrl, {'login': username, 'password': self.env.user.credential})['token']
            self.env.user.rpc_token = token
        response = Spreadsheet.new_spreadsheet(baseUrl, self.file_name, self.attachment_id, self.env.user.rpc_token)
        self.path = response['path']
        return self.redirect_url(response['path'])
