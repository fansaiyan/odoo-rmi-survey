from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied


class CustomAPIController(http.Controller):

    @http.route('/custom_api/login', type='http', auth="none", methods=['POST'], csrf=False)
    def login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return http.Response('Username and password are required.', status=400)

        uid = request.session.authenticate(request.db, username, password)
        if not uid:
            raise AccessDenied()

        return http.Response('Login successful! User ID: {}'.format(uid))
