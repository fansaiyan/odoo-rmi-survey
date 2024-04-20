from odoo import http
from odoo.http import request, Response
import json
class CustomAPIController(http.Controller):
    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/api/survey-list', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_pajak(self, **kw):
        data = []
        query = """
            select
                s.id,
                (s.title->>'en_US')::varchar AS nama,
                s.user_id,
                s.company_id
                from survey_survey as s
        """
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            data.append(row_dict)
        headers = {'Content-Type': 'application/json'}
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)