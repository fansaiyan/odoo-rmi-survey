from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied
from odoo.http import request, Response
import json
class CustomAPIController(http.Controller):

    @http.route('/custom_api/login', website=False, auth='public', type="http", csrf=False, methods=['POST'])
    def login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')

        if not username or not password:
            return http.Response('Username and password are required.', status=400)

        uid = request.session.authenticate(request.db, username, password)
        if not uid:
            raise AccessDenied()

        return http.Response('Login successful! User ID: {}'.format(uid))

    @http.route('/api/rmi_param_group', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_pajak(self, **kw):
        row_list = []
        rows = request.env['rmi.param_group'].sudo().search([])[0]
        if len(rows) > 0:
            for row in rows:
                row_list.append({
                    'name': row.name
                })
        headers = {'Content-Type': 'application/json'}
        body = {'results': {'code': 200, 'message': 'OK', 'data': row_list}}
        return Response(json.dumps(body), headers=headers)