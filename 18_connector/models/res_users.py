from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    use_login = fields.Boolean('User Login Info')
    username = fields.Char('Login')
    credential = fields.Char('Password')
    rpc_token = fields.Char('Token')
