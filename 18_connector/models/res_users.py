from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _redirect_url(self):
        print('redirect url')
        return {
            'name': 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'www.google.com'
        }
