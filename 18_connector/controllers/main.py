from odoo import http
from odoo.http import request
import werkzeug


class Main(http.Controller):

    @http.route("/auth/signin", type="http", auth="public",)
    def auto_login_redirect_link(self):
        baseUrl = request.env['ir.config_parameter'].sudo().get_param('18.base.url')
        login = request.env['ir.config_parameter'].sudo().get_param('connector.email')
        passwd = request.env['ir.config_parameter'].sudo().get_param('connector.pwd')
        return werkzeug.redirect(f'{baseUrl}?username={login}&password={passwd}')