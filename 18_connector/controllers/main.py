from odoo import http
from odoo.http import request
from passlib.context import CryptContext
import logging
_logger = logging.getLogger(__name__)

pwd_cryptcontext = CryptContext(
    ['pbkdf2_sha512'], pbkdf2_sha512__rounds=6000,
)


class Main(http.Controller):

    @http.route("/auth/signin", type="http", auth="none", )
    def auto_login_redirect_link(self, redirect=None):
        if not redirect:
            redirect = '/web'
        _logger.inf(f'redirect url ---- {redirect}')
        baseUrl = request.env['ir.config_parameter'].sudo().get_param('18.base.url')
        user = request.env['res.users'].sudo().browse(request.session.uid)
        return http.local_redirect(f'{baseUrl}/auth/signin', query={'name': user.name,
                                                                    'login': user.login,
                                                                    'password': user.credential,
                                                                    'redirect': redirect}, keep_hash=True)
