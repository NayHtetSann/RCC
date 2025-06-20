from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    connector_base_url = fields.Char(string='18 Base Url', config_parameter='18.base.url')
    connector_email = fields.Char(string='Connector Email', config_parameter='connector.email')
    connector_pwd = fields.Char(string='Connector Password', config_parameter='connector.pwd')
