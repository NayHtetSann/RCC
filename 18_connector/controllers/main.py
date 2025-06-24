from odoo import http
from odoo.http import request
from passlib.context import CryptContext
import werkzeug

pwd_cryptcontext = CryptContext(
    ['pbkdf2_sha512'], pbkdf2_sha512__rounds=6000,
)


class Main(http.Controller):

    @http.route("/auth/signin", type="http", auth="none", )
    def auto_login_redirect_link(self):
        baseUrl = request.env['ir.config_parameter'].sudo().get_param('18.base.url')
        print(baseUrl)
        print(request.env.user, request.uid, request.session,'what the hell')
        user = request.env['res.users'].sudo().browse(request.session.uid)
        return http.local_redirect(f'{baseUrl}', query={'name': user.name,
                                                        'login': user.login,
                                                        'password': user.credential}, keep_hash=True)
        # return werkzeug.redirect(f'{baseUrl}?username={request.env.user.login}&password={request.env.user.credential}')
