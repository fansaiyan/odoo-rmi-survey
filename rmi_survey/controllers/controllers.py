from odoo import http
from odoo.http import request, Response
import json
import io
from datetime import datetime

class CustomAPIController(http.Controller):
    @http.route('/web/session/authenticate', type='json', auth="none", cors="*")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

    @http.route('/api/parameter-dimensi', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_parameter_dimensi(self, **kwargs):
        data = []
        query = """
                select * from rmi_param_dimensi
            """
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/parameter-group', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_parameter_group(self, **kwargs):
        data = []
        query = """
                   select g.*, d.id as dimensi_id, d.name as dimensi_name
                    from rmi_param_group as g
                    left join rmi_param_dimensi as d on d.id = g.param_dimensi
                """
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/final-rating', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_final_rating(self, **kwargs):
        data = []
        query = """
                        select * from rmi_final_rating
                    """
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/komposit-resiko', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_komposite_resiko(self, **kwargs):
        data = []
        query = """
                           select * from rmi_komposit_risiko
                       """
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)
    @http.route('/api/survey-list', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_survey_list(self, **kwargs):
        data = []
        company_id = kwargs.get('company_id', None)
        query = """
             select
                s.id,
                (s.title->>'en_US')::varchar AS name,
                s.user_id,
                s.company_id,
                s.periode,
                s.jenis_industri,
                c.name as company_name
                from survey_survey as s
                left join res_company as c on c.id = s.company_id
        """
        if company_id:
            query += f" where s.company_id = {company_id}"

        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/survey-by-id/<int:id>', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_survey_by_id(self, id, **kwargs):
        data = []
        query = """
                 select
                    s.id,
                    (s.title->>'en_US')::varchar AS name,
                    s.user_id,
                    s.company_id,
                    s.periode,
                    s.jenis_industri,
                    c.name as company_name
                    from survey_survey as s
                    left join res_company as c on c.id = s.company_id 
                    where s.id = {}
                    """.format(id)
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/aspek-kinerja-list', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_aspek_kinerja_list(self, **kwargs):
        data = []
        company_id = kwargs.get('company_id', None)
        query = """
                 select
                    ROW_NUMBER() OVER () AS no,
                    a.*,
                    (b.title ->>'en_US')::varchar AS survey_name,
                    b.periode,
                    b.jenis_industri,
                    c.name as company_name
                from rmi_aspek_kinerja as a
                left join survey_survey as b on b.id = a.survey_ids
                left join res_company as c on c.id = b.company_id
            """
        if company_id:
            query += f" where b.company_id = {company_id}"
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/aspek-kinerja-by-id/<int:id>', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_aspek_kinerja_by_id(self, id, **kwargs):
        data = []
        query = """
                     select
                        ROW_NUMBER() OVER () AS no,
                        a.*,
                        (b.title ->>'en_US')::varchar AS survey_name,
                        b.periode,
                        b.jenis_industri,
                        c.name as company_name
                    from rmi_aspek_kinerja as a
                    left join survey_survey as b on b.id = a.survey_ids
                    left join res_company as c on c.id = b.company_id
                    where a.id = {}
                """.format(id)
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/aspek-kinerja-delete/<int:id>', website=False, auth='public', type="http", csrf=False,
                methods=['DELETE'], cors="*")
    def _get_aspek_kinerja_delete(self, id, **kwargs):
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Credentials': 'true'
        }
        try:
            data = request.env['rmi.aspek_kinerja'].sudo().search([('id', '=', id)], limit=1)
            if data is None:
                errorMsg = f"Data Tidak Ditemukan"
                body = {
                    'status': 500,
                    'message': errorMsg,
                    'execution_time': '0s'
                }
            else:
                if data.unlink():
                    body = {'status': 200, 'message': 'OK', 'data': None}
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': 500,
                'message': errorMsg,
                'execution_time': '0s'
            }
            # body = {'status': 200, 'message': 'OK', 'data': payload}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/aspek-kinerja-create', website=False, auth='public', type="http", csrf=False, methods=['POST'], cors="*")
    def post_aspek_kinerja_create(self, **kwargs):
        body = io.BytesIO(request.httprequest.data)
        payload = json.load(body)
        id = None
        if payload['id'] != 0:
            id = payload['id']
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            # 'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true'
        }
        try:
            survey = request.env['survey.survey'].sudo().search([('id', '=', payload['survey_ids'])], limit=1)
            postBody = {
                'create_uid': payload['uid'],
                'write_uid': payload['uid'],
                'name': payload['name'],
                'aspect_values': payload['aspect_value'],
                'composite_risk_levels': payload['composite_risk_levels'],
                'final_rating_weight': payload['final_rating_weight'],
                'composite_risk_weight': payload['composite_risk_weight'],
                'company_name': survey.company_id.name,
                'score_adjustment': payload['score_adjustment'],
                'survey_ids': payload['survey_ids'],
                'state': 'done'
            }
            if id is not None:
                existing_record = request.env['rmi.aspek_kinerja'].sudo().browse(id)
                existing_record.write(postBody)
                body = {'status': 200, 'message': 'OK', 'data': None}
            else:
                insert = request.env['rmi.aspek_kinerja'].sudo().create(postBody)
                if insert.id:
                    body = {'status': 200, 'message': 'OK', 'data': None}
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': 500,
                'message': errorMsg,
                'execution_time': '0s'
            }
            # body = {'status': 200, 'message': 'OK', 'data': payload}
        return Response(json.dumps(body), headers=headers)

    @http.route('/api/aspek-kinerja/<int:id>', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _get_aspek_kinerja_detaila(self, id,  **kwargs):
        data = []
        query = """
                 WITH CombinedData AS (
                    select
                        a.id as aspek_id,
                        'Tingkat Kesehatan Peringkat' as aspek,
                        fr.name as nilai_aspek,
                        fr.nilai as nilai_konversi_aspek,
                        a.final_rating_weight as bobot,
                        ROUND((fr.nilai * a.final_rating_weight) / 100::NUMERIC, 1) as nilai_konversi,
                        a.survey_ids
                        from rmi_aspek_kinerja as a
                        left join rmi_final_rating as fr on fr.id = a.aspect_values
                    UNION ALL
                    select
                        a.id as aspek_id,
                        'Peringkat Komposit Resiko' as aspek,
                        kr.name as nilai_aspek,
                        kr.nilai as nilai_konversi_aspek,
                        a.composite_risk_weight as bobot,
                        ROUND((kr.nilai * a.composite_risk_weight) / 100::NUMERIC, 1) as nilai_konversi,
                        a.survey_ids
                        from rmi_aspek_kinerja as a
                        left join rmi_komposit_risiko as kr on kr.id = a.composite_risk_levels
                )
                SELECT
                    ROW_NUMBER() OVER () AS No, aspek_id,
                    survey_ids, aspek, nilai_aspek, nilai_konversi_aspek, bobot, nilai_konversi
                    FROM CombinedData where aspek_id = {}
                """.format(id)
        http.request.env.cr.execute(query)
        fetched_data = http.request.env.cr.fetchall()
        column_names = [desc[0] for desc in http.request.env.cr.description]
        for row in fetched_data:
            row_dict = dict(zip(column_names, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = str(value)
            data.append(row_dict)
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        body = {'status': 200, 'message': 'OK', 'data': data}
        return Response(json.dumps(body), headers=headers)
    @http.route('/api/report/adjust-aspek-dimensi', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _adjust_aspek_dimensi(self, **kwargs):
        survey_id = kwargs.get('survey_id', None)
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                      select
                        ROW_NUMBER() OVER () AS no,
                        (ss.title->>'en_US')::varchar AS survey_name,
                        a.survey_id,
                        h.name as company,
                        a.question_id as question_id,
                        i.name as dimensi,
                        j.name as subdimensi,
                        (b.title->>'en_US')::varchar AS parameterName,
                        avg((e.value->>'en_US')::int) as avgvalue,
                        min((e.value->>'en_US')::int) as minvalue,
                        max((e.value->>'en_US')::int) as maxvalue,
                        max((e.value->>'en_US')::int) - min((e.value->>'en_US')::int) as rangevalue,
                        mode() WITHIN GROUP (ORDER BY (e.value->>'en_US')::int) AS mod
                        from survey_user_input_line as a
                        left join survey_question as b on a.question_id = b.id
                        left join survey_user_input as c on c.id = a.user_input_id
                        left join res_partner as d on d.id = c.partner_id
                        left join survey_question_answer as e on e.id = a.suggested_answer_id
                        left join res_users as f on f.partner_id = d.id
                        left join hr_employee as g on g.user_id = f.id
                        left join res_company as h on h.id = g.company_id
                        left join rmi_param_dimensi as i on i.id = b.dimensi_names
                        left join rmi_param_group as j on j.id = b.sub_dimensi_names
                        left join survey_survey as ss on ss.id = a.survey_id
                    where a.survey_id = {} and c.state = 'done' and a.suggested_answer_id is not null
                    GROUP BY a.question_id, parameterName, company, i.name, j.name, survey_name, a.survey_id
                    ORDER BY a.question_id ASC
                   """.format(survey_id)
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/adjust-aspek-dimensi-perdimensi', website=False, auth='public', type="http", csrf=False,
                methods=['GET'])
    def _adjust_aspek_dimensi_perdimensi(self, **kwargs):
        survey_id = kwargs.get('survey_id', None)
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                      select
                            ROW_NUMBER() OVER () AS no,
                            subq.survey_name,
                            subq.survey_id,
                            subq.company,
                            subq.dimensi,
                            subq.dimensi_id,
                            ROUND(AVG(subq.avg), 2) AS avg
                            from
                            (
                                select
                                    (ss.title->>'en_US')::varchar AS survey_name,
                                    a.survey_id,
                                    h.name as company,
                                    i.name as dimensi,
                                    i.id as dimensi_id,
                                    ROUND(MIN((e.value->>'en_US')::int), 2) AS avg
                                    from survey_user_input_line as a
                                    left join survey_question as b on a.question_id = b.id
                                    left join survey_user_input as c on c.id = a.user_input_id
                                    left join res_partner as d on d.id = c.partner_id
                                    left join survey_question_answer as e on e.id = a.suggested_answer_id
                                    left join res_users as f on f.partner_id = d.id
                                    left join hr_employee as g on g.user_id = f.id
                                    left join res_company as h on h.id = g.company_id
                                    left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                    left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                    left join survey_survey as ss on ss.id = a.survey_id
                                where a.survey_id = {} and c.state = 'done' and a.suggested_answer_id is not null
                                GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id, ss.title, h.name
                                ORDER BY a.question_id ASC
                            ) as subq
                        GROUP BY subq.survey_name, subq.survey_id, subq.company, subq.dimensi, subq.dimensi_id
                        ORDER BY subq.dimensi_id
                       """.format(survey_id)
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/adjust-aspek-dimensi-persubdimensi', website=False, auth='public', type="http", csrf=False,
                methods=['GET'])
    def _adjust_aspek_dimensi_persubdimensi(self, **kwargs):
        survey_id = kwargs.get('survey_id', None)
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                  select
                    ROW_NUMBER() OVER () AS no,
                    subq.survey_name,
                    subq.survey_id,
                    subq.company,
                    subq.dimensi,
                    subq.subdimensi,
                    subq.subdimensi_id,
                    ROUND(avg(subq.avgparamter), 2) as avg
                    from
                    (
                        select
                            (ss.title->>'en_US')::varchar AS survey_name,
                            a.survey_id,
                            h.name as company,
                            i.name as dimensi,
                            j.name as subdimensi,
                            (b.title->>'en_US')::varchar AS parameterName,
                            avg((e.value->>'en_US')::int) as avgparamter,
                            j.id as subdimensi_id
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                        where a.survey_id = {} and c.state = 'done' and a.suggested_answer_id is not null
                        GROUP BY a.question_id, parameterName, company, i.name, j.name, survey_name, a.survey_id, j.id
                        ORDER BY a.question_id ASC
                    ) as subq
                GROUP BY  subq.subdimensi,subq.survey_name, subq.survey_id, subq.company, subq.dimensi, subq.subdimensi, subq.subdimensi_id
                ORDER BY subq.subdimensi_id
                           """.format(survey_id)
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/interest-coverage-ratio-by-rate', website=False, auth='public', type="http", csrf=False,
                methods=['GET'])
    def _interest_coverage_ratio_by_rate(self, **kwargs):
        rate = kwargs.get('rate', None)
        data = []
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not rate:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "rate" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                      SELECT *
                            FROM rmi_icr
                            WHERE {} BETWEEN min AND max
                               """.format(rate)
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/interest-coverage-ratio', website=False, auth='public', type="http", csrf=False,
                methods=['GET'])
    def _interest_coverage_ratio(self, **kwargs):
        data = []
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        try:
            query = """SELECT * FROM rmi_icr"""
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/adjust-aspek-dimensi-detail', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _adjust_aspek_dimensi_detail(self, **kwargs):
        survey_id = kwargs.get('survey_id', None)
        question_id = kwargs.get('question_id', None)
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id or not question_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                  select
                    ROW_NUMBER() OVER () AS No,
                    a.question_id,
                    h.name as company,
                    (b.title->>'en_US')::varchar AS parameterName,
                    d.name as user,
                    i.name as Department,
                    (e.value->>'en_US')::int AS value
                    from survey_user_input_line as a
                    left join survey_question as b on a.question_id = b.id
                    left join survey_user_input as c on c.id = a.user_input_id
                    left join res_partner as d on d.id = c.partner_id
                    left join survey_question_answer as e on e.id = a.suggested_answer_id
                    left join res_users as f on f.partner_id = d.id
                    left join hr_employee as g on g.user_id = f.id
                    left join res_company as h on h.id = g.company_id
                    left join hr_department as i on i.id = g.department_id
                where a.survey_id = {} and c.state = 'done' and a.question_id = {} and a.suggested_answer_id is not null
               """.format(survey_id, question_id)
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/adjust-aspek-dimensi-detail-all-rows', website=False, auth='public', type="http", csrf=False,
                methods=['GET'])
    def _adjust_aspek_dimensi_detail_all_rows(self, **kwargs):
        survey_id = kwargs.get('survey_id', None)
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                      select
                            ROW_NUMBER() OVER () AS no,
                            subquery.survey_name,
                            subquery.question_id,
                            subquery.survey_id,
                            subquery.company,
                            subquery.dimensi,
                            subquery.subdimensi,
                            subquery.parameterName,
                            subquery.user,
                            subquery.Department,
                            subquery.value,
                            subquery.filename
                            from (
                                select
                                    (ss.title->>'en_US')::varchar AS survey_name,
                                    a.question_id ,
                                    a.survey_id,
                                    h.name as company,
                                    i.name as dimensi,
                                    j.name as subdimensi,
                                    j.id as subdimensi_id,
                                    (b.title->>'en_US')::varchar AS parameterName,
                                    d.name as user,
                                    hr.name as Department,
                                    (e.value->>'en_US')::int AS value,
                                    sqa.value_char_box as filename
                                    from survey_user_input_line as a
                                    left join survey_question as b on a.question_id = b.id
                                    left join survey_user_input as c on c.id = a.user_input_id
                                    left join res_partner as d on d.id = c.partner_id
                                    left join survey_question_answer as e on e.id = a.suggested_answer_id
                                    left join res_users as f on f.partner_id = d.id
                                    left join hr_employee as g on g.user_id = f.id
                                    left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                    left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                    left join survey_survey as ss on ss.id = a.survey_id
                                    left join res_company as h on h.id = ss.company_id
                                    left join hr_department as hr on hr.id = g.department_id
                                    left join survey_user_input_line as sqa on sqa.question_id = a.question_id and sqa.suggested_answer_id is null and sqa.write_uid = f.id
                                    where a.survey_id = {} and c.state = 'done' and a.suggested_answer_id is not null order by subdimensi_id
                                 ) as subquery
                   """.format(survey_id)
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)
    @http.route('/api/report/aspek-dimensi', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _aspek_dimensi_corporate(self, **kwargs):
        survey_id = kwargs.get('survey_id', None)
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                      select
                            ROW_NUMBER() OVER () AS no,
                            subq.parameter,
                            subq.dimensi,
                            subq.deskripsi,
                            ROUND(AVG(subq.minvalue), 2) AS skordimensi,
                            subq.skor_max
                            from
                            (
                                select
                                    CASE
                                        WHEN i.name = 'Budaya dan Kapabilitas Risiko' THEN '1 s.d. 3'
                                        WHEN i.name = 'Organisasi dan Tata Kelola Risiko' THEN '4 s.d. 19'
                                        WHEN i.name = 'Kerangka Risiko dan Kepatuhan' THEN '20 s.d. 33'
                                        WHEN i.name = 'Proses dan Kontrol Risiko' THEN '34 s.d. 39'
                                        ELSE '40 s.d. 42'
                                    END as parameter,
                                    i.param_dimensi_id as dimensi,
                                    i.name as deskripsi,
                                    ROUND(MIN((e.value->>'en_US')::int), 2) AS minvalue,
                                    5 as skor_max
                                    from survey_user_input_line as a
                                    left join survey_question as b on a.question_id = b.id
                                    left join survey_user_input as c on c.id = a.user_input_id
                                    left join res_partner as d on d.id = c.partner_id
                                    left join survey_question_answer as e on e.id = a.suggested_answer_id
                                    left join res_users as f on f.partner_id = d.id
                                    left join hr_employee as g on g.user_id = f.id
                                    left join res_company as h on h.id = g.company_id
                                    left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                    left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                    left join survey_survey as ss on ss.id = a.survey_id
                                where a.survey_id = {} and c.state = 'done' and a.suggested_answer_id is not null
                                GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id
                                ORDER BY a.question_id ASC
                            ) as subq
                        GROUP BY subq.dimensi, subq.parameter, subq.deskripsi, subq.skor_max
                        ORDER BY subq.dimensi
                   """.format(survey_id)
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/hasil-penilaian-rmi', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _report_hasil_penilaian_rmi(self, **kwargs):
        survey_id = kwargs.get('survey_id', None)
        aspek_id = kwargs.get('aspek_id', None)
        data = {
            "summary": [],
            "dimensi": [],
            'kinerja': []
        }
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query_summary = """
                select
                    c.name as company,
                    b.periode,
                    a.no_laporan,
                    b.jenis_industri
                from rmi_aspek_kinerja as a
                left join survey_survey as b on b.id = a.survey_ids
                left join res_company as c on c.id = b.company_id
                where a.id = {} and a.survey_ids = {}
                   """.format(aspek_id, survey_id)
            http.request.env.cr.execute(query_summary)
            fetched_data_summary = http.request.env.cr.fetchall()
            column_names_summary = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data_summary:
                row_dict = dict(zip(column_names_summary, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data['summary'].append(row_dict)
            query_dimensi = """
                          select
                            ROW_NUMBER() OVER () AS no,
                            subq.parameter,
                            subq.dimensi,
                            subq.deskripsi,
                            ROUND(avg(subq.minvalue::int), 2) as skordimensi
                            from
                            (
                                select
                                    CASE
                                        WHEN i.name = 'Budaya dan Kapabilitas Risiko' THEN '1 s.d. 3'
                                        WHEN i.name = 'Organisasi dan Tata Kelola Risiko' THEN '4 s.d. 19'
                                        WHEN i.name = 'Kerangka Risiko dan Kepatuhan' THEN '20 s.d. 33'
                                        WHEN i.name = 'Proses dan Kontrol Risiko' THEN '34 s.d. 39'
                                        ELSE '40 s.d. 42'
                                    END as parameter,
                                    i.param_dimensi_id as dimensi,
                                    i.name as deskripsi,
                                    min((e.value->>'en_US')::int) as minvalue
                                    from survey_user_input_line as a
                                    left join survey_question as b on a.question_id = b.id
                                    left join survey_user_input as c on c.id = a.user_input_id
                                    left join res_partner as d on d.id = c.partner_id
                                    left join survey_question_answer as e on e.id = a.suggested_answer_id
                                    left join res_users as f on f.partner_id = d.id
                                    left join hr_employee as g on g.user_id = f.id
                                    left join res_company as h on h.id = g.company_id
                                    left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                    left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                    left join survey_survey as ss on ss.id = a.survey_id
                                where a.survey_id = {} and c.state = 'done' and a.suggested_answer_id is not null
                                GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id
                                ORDER BY a.question_id ASC
                            ) as subq
                        GROUP BY subq.dimensi, subq.parameter, subq.deskripsi
                        ORDER BY subq.dimensi
                       """.format(survey_id)
            http.request.env.cr.execute(query_dimensi)
            fetched_data_dimensi = http.request.env.cr.fetchall()
            column_names_dimensi = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data_dimensi:
                row_dict = dict(zip(column_names_dimensi, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data['dimensi'].append(row_dict)
            query_kinerja = """
                      WITH CombinedData AS (
                        select
                            a.id as aspek_id,
                            'Tingkat Kesehatan Peringkat' as aspek,
                            fr.name as nilai_aspek,
                            fr.nilai as nilai_konversi_aspek,
                            a.final_rating_weight as bobot,
                            ROUND((fr.nilai * a.final_rating_weight) / 100::NUMERIC, 1) as nilai_konversi,
                            a.survey_ids
                            from rmi_aspek_kinerja as a
                            left join rmi_final_rating as fr on fr.id = a.aspect_values
                        UNION ALL
                        select
                            a.id as aspek_id,
                            'Peringkat Komposit Resiko' as aspek,
                            kr.name as nilai_aspek,
                            kr.nilai as nilai_konversi_aspek,
                            a.composite_risk_weight as bobot,
                            ROUND((kr.nilai * a.composite_risk_weight) / 100::NUMERIC, 1) as nilai_konversi,
                            a.survey_ids
                            from rmi_aspek_kinerja as a
                            left join rmi_komposit_risiko as kr on kr.id = a.composite_risk_levels
                    )
                    SELECT
                        ROW_NUMBER() OVER () AS No, aspek_id,
                        survey_ids, aspek, nilai_aspek, nilai_konversi_aspek, bobot, nilai_konversi
                        FROM CombinedData where survey_ids = {} and aspek_id = {}
                                   """.format(survey_id, aspek_id)
            http.request.env.cr.execute(query_kinerja)
            fetched_data_kinerja = http.request.env.cr.fetchall()
            column_names_kinerja = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data_kinerja:
                row_dict = dict(zip(column_names_kinerja, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data['kinerja'].append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/chart1', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _chart1(self, **kwargs):
        survey_id = kwargs.get('survey_id')
        periode = kwargs.get('periode')
        jenis_industri = kwargs.get('jenis_industri')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                (
                SELECT
                    subq.survey_key,
                    subq.survey_name,
                    subq.jenis_industri,
                    ROUND(AVG(CASE WHEN subq.dimensi_id = 1 THEN subq.avg END), 2) AS dimensi_1,
                    ROUND(AVG(CASE WHEN subq.dimensi_id = 2 THEN subq.avg END), 2) AS dimensi_2,
                    ROUND(AVG(CASE WHEN subq.dimensi_id = 3 THEN subq.avg END), 2) AS dimensi_3,
                    ROUND(AVG(CASE WHEN subq.dimensi_id = 4 THEN subq.avg END), 2) AS dimensi_4,
                    ROUND(AVG(CASE WHEN subq.dimensi_id = 5 THEN subq.avg END), 2) AS dimensi_5
                FROM (
                    SELECT
                        'sur-' || CAST(ss.id as TEXT) as survey_key,
                        ss.title->>'en_US' AS survey_name,
                        i.id AS dimensi_id,
                        ROUND(MIN((e.value->>'en_US')::int), 2) AS avg,
                        ss.jenis_industri
                    FROM survey_user_input_line AS a
                    LEFT JOIN survey_question AS b ON a.question_id = b.id
                    LEFT JOIN survey_user_input AS c ON c.id = a.user_input_id
                    LEFT JOIN res_partner AS d ON d.id = c.partner_id
                    LEFT JOIN survey_question_answer AS e ON e.id = a.suggested_answer_id
                    LEFT JOIN res_users AS f ON f.partner_id = d.id
                    LEFT JOIN hr_employee AS g ON g.user_id = f.id
                    LEFT JOIN res_company AS h ON h.id = g.company_id
                    LEFT JOIN rmi_param_dimensi AS i ON i.id = b.dimensi_names
                    LEFT JOIN rmi_param_group AS j ON j.id = b.sub_dimensi_names
                    LEFT JOIN survey_survey AS ss ON ss.id = a.survey_id
                    WHERE c.state = 'done'
                      AND a.suggested_answer_id IS NOT NULL and ss.id = """+survey_id+"""
                    GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id, ss.title, h.name, ss.id
                    ORDER BY a.question_id ASC
                ) AS subq
                GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                ORDER BY subq.survey_name
                )
                UNION ALL
                (
                    SELECT
                    subq.survey_key,
                    subq.survey_name,
                    subq.jenis_industri,
                    ROUND(MAX(CASE WHEN subq.dimensi_id = 1 THEN subq.avg END), 2) AS dimensi_1,
                    ROUND(MAX(CASE WHEN subq.dimensi_id = 2 THEN subq.avg END), 2) AS dimensi_2,
                    ROUND(MAX(CASE WHEN subq.dimensi_id = 3 THEN subq.avg END), 2) AS dimensi_3,
                    ROUND(MAX(CASE WHEN subq.dimensi_id = 4 THEN subq.avg END), 2) AS dimensi_4,
                    ROUND(MAX(CASE WHEN subq.dimensi_id = 5 THEN subq.avg END), 2) AS dimensi_5
                    FROM (
                        SELECT
                            'max-01'as survey_key,
                            'MAX INDUSTRI """+jenis_industri+"""' AS survey_name,
                             i.id AS dimensi_id,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg,
                            'MAX """+jenis_industri+"""' as jenis_industri
                        FROM survey_user_input_line AS a
                        LEFT JOIN survey_question AS b ON a.question_id = b.id
                        LEFT JOIN survey_user_input AS c ON c.id = a.user_input_id
                        LEFT JOIN res_partner AS d ON d.id = c.partner_id
                        LEFT JOIN survey_question_answer AS e ON e.id = a.suggested_answer_id
                        LEFT JOIN res_users AS f ON f.partner_id = d.id
                        LEFT JOIN hr_employee AS g ON g.user_id = f.id
                        LEFT JOIN res_company AS h ON h.id = g.company_id
                        LEFT JOIN rmi_param_dimensi AS i ON i.id = b.dimensi_names
                        LEFT JOIN rmi_param_group AS j ON j.id = b.sub_dimensi_names
                        LEFT JOIN survey_survey AS ss ON ss.id = a.survey_id
                        WHERE c.state = 'done'
                          AND a.suggested_answer_id IS NOT NULL AND ss.jenis_industri = '"""+jenis_industri+"""' -- parameter seusuaikan jenis industri pada servey yg di pilih
                          AND ss.periode = '"""+periode+"""'
                        GROUP BY i.name, survey_name, a.survey_id, j.id, i.id, ss.jenis_industri, ss.id
                        ORDER BY j.id ASC
                    ) AS subq
                    GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                    ORDER BY subq.survey_name
                )
                UNION ALL
                (
                        SELECT
                        subq.survey_key,
                        subq.survey_name,
                        subq.jenis_industri,
                        ROUND(MAX(CASE WHEN subq.dimensi_id = 1 THEN subq.avg END), 2) AS dimensi_1,
                        ROUND(MAX(CASE WHEN subq.dimensi_id = 2 THEN subq.avg END), 2) AS dimensi_2,
                        ROUND(MAX(CASE WHEN subq.dimensi_id = 3 THEN subq.avg END), 2) AS dimensi_3,
                        ROUND(MAX(CASE WHEN subq.dimensi_id = 4 THEN subq.avg END), 2) AS dimensi_4,
                        ROUND(MAX(CASE WHEN subq.dimensi_id = 5 THEN subq.avg END), 2) AS dimensi_5
                    FROM (
                        SELECT
                            'max-02' as survey_key,
                            'MAX ALL DATA' AS survey_name,
                             i.id AS dimensi_id,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg,
                            'MAX ALL DATA' as jenis_industri
                        FROM survey_user_input_line AS a
                        LEFT JOIN survey_question AS b ON a.question_id = b.id
                        LEFT JOIN survey_user_input AS c ON c.id = a.user_input_id
                        LEFT JOIN res_partner AS d ON d.id = c.partner_id
                        LEFT JOIN survey_question_answer AS e ON e.id = a.suggested_answer_id
                        LEFT JOIN res_users AS f ON f.partner_id = d.id
                        LEFT JOIN hr_employee AS g ON g.user_id = f.id
                        LEFT JOIN res_company AS h ON h.id = g.company_id
                        LEFT JOIN rmi_param_dimensi AS i ON i.id = b.dimensi_names
                        LEFT JOIN rmi_param_group AS j ON j.id = b.sub_dimensi_names
                        LEFT JOIN survey_survey AS ss ON ss.id = a.survey_id
                        WHERE c.state = 'done'
                          AND a.suggested_answer_id IS NOT NULL
                          AND ss.periode = '"""+periode+"""'
                        GROUP BY i.name, survey_name, a.survey_id, j.id, i.id, ss.jenis_industri, ss.id
                        ORDER BY j.id ASC
                    ) AS subq
                    GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                    ORDER BY subq.survey_name
                )
                UNION ALL
                select
                    'max-03' as survey_key,
                    'MAX' as survey_name,
                    'MAX' as jenis_industri,
                    5 AS dimensi_1,
                    5 AS dimensi_2,
                    5 AS dimensi_3,
                    5 AS dimensi_4,
                    5 AS dimensi_5
                       """
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/chart2', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _chart2(self, **kwargs):
        survey_id = kwargs.get('survey_id')
        periode = kwargs.get('periode')
        jenis_industri = kwargs.get('jenis_industri')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                (
                    SELECT
                        subq.survey_key,
                        subq.survey_name,
                        subq.jenis_industri,
                        ROUND(AVG(CASE WHEN subq.parameter = 'Internalisasi budaya risiko dalam budaya perusahaan' THEN subq.avg END), 2) AS parameter_1,
                        ROUND(AVG(CASE WHEN subq.parameter = 'Peran Penilaian RMI dalam upaya peningkatan praktik Manajemen Risiko' THEN subq.avg END), 2) AS parameter_2,
                        ROUND(AVG(CASE WHEN subq.parameter = 'Program peningkatan keahlian Risiko' THEN subq.avg END), 2) AS parameter_3
                    FROM (
                        select
                        'sur-' || CAST(ss.id as TEXT) as survey_key,
                        (ss.title->>'en_US')::varchar AS survey_name,
                        ss.jenis_industri,
                        (b.title->>'en_US')::varchar AS parameter,
                        ROUND(MIN((e.value->>'en_US')::int), 2) AS avg
                        from survey_user_input_line as a
                        left join survey_question as b on a.question_id = b.id
                        left join survey_user_input as c on c.id = a.user_input_id
                        left join res_partner as d on d.id = c.partner_id
                        left join survey_question_answer as e on e.id = a.suggested_answer_id
                        left join res_users as f on f.partner_id = d.id
                        left join hr_employee as g on g.user_id = f.id
                        left join res_company as h on h.id = g.company_id
                        left join rmi_param_dimensi as i on i.id = b.dimensi_names
                        left join rmi_param_group as j on j.id = b.sub_dimensi_names
                        left join survey_survey as ss on ss.id = a.survey_id
                        where a.survey_id = """+survey_id+""" and c.state = 'done' and a.suggested_answer_id is not null
                        and i.id = 1
                        and ss.periode = '"""+periode+"""'
                        GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id, ss.title, h.name, ss.id, b.title
                        ORDER BY a.question_id ASC
                    ) AS subq
                    GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                    ORDER BY subq.survey_name
                )
                UNION ALL
                (
                    SELECT
                        subq.survey_key,
                        subq.survey_name,
                        subq.jenis_industri,
                        ROUND(MAX(CASE WHEN subq.parameter = 'Internalisasi budaya risiko dalam budaya perusahaan' THEN subq.avg END), 2) AS parameter_1,
                        ROUND(MAX(CASE WHEN subq.parameter = 'Peran Penilaian RMI dalam upaya peningkatan praktik Manajemen Risiko' THEN subq.avg END), 2) AS parameter_2,
                        ROUND(MAX(CASE WHEN subq.parameter = 'Program peningkatan keahlian Risiko' THEN subq.avg END), 2) AS parameter_3
                    FROM (
                        select
                        'max-01'as survey_key,
                        'MAX INDUSTRI """+jenis_industri+"""' AS survey_name,
                        (b.title->>'en_US')::varchar AS parameter,
                        'MAX """+jenis_industri+"""' as jenis_industri,
                        ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                        from survey_user_input_line as a
                        left join survey_question as b on a.question_id = b.id
                        left join survey_user_input as c on c.id = a.user_input_id
                        left join res_partner as d on d.id = c.partner_id
                        left join survey_question_answer as e on e.id = a.suggested_answer_id
                        left join res_users as f on f.partner_id = d.id
                        left join hr_employee as g on g.user_id = f.id
                        left join res_company as h on h.id = g.company_id
                        left join rmi_param_dimensi as i on i.id = b.dimensi_names
                        left join rmi_param_group as j on j.id = b.sub_dimensi_names
                        left join survey_survey as ss on ss.id = a.survey_id
                        where c.state = 'done' and a.suggested_answer_id is not null
                        and i.id = 1
                        and ss.periode = '"""+periode+"""'
                        and ss.jenis_industri = '"""+jenis_industri+"""'
                        GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                        ORDER BY a.question_id ASC
                    ) AS subq
                    GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                    ORDER BY subq.survey_name
                )
                UNION ALL
                (
                    SELECT
                        subq.survey_key,
                        subq.survey_name,
                        subq.jenis_industri,
                        ROUND(MAX(CASE WHEN subq.parameter = 'Internalisasi budaya risiko dalam budaya perusahaan' THEN subq.avg END), 2) AS parameter_1,
                        ROUND(MAX(CASE WHEN subq.parameter = 'Peran Penilaian RMI dalam upaya peningkatan praktik Manajemen Risiko' THEN subq.avg END), 2) AS parameter_2,
                        ROUND(MAX(CASE WHEN subq.parameter = 'Program peningkatan keahlian Risiko' THEN subq.avg END), 2) AS parameter_3
                    FROM (
                        select
                        'max-01'as survey_key,
                        'MAX ALL DATA' AS survey_name,
                        (b.title->>'en_US')::varchar AS parameter,
                        'MAX ALL DATA' as jenis_industri,
                        ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                        from survey_user_input_line as a
                        left join survey_question as b on a.question_id = b.id
                        left join survey_user_input as c on c.id = a.user_input_id
                        left join res_partner as d on d.id = c.partner_id
                        left join survey_question_answer as e on e.id = a.suggested_answer_id
                        left join res_users as f on f.partner_id = d.id
                        left join hr_employee as g on g.user_id = f.id
                        left join res_company as h on h.id = g.company_id
                        left join rmi_param_dimensi as i on i.id = b.dimensi_names
                        left join rmi_param_group as j on j.id = b.sub_dimensi_names
                        left join survey_survey as ss on ss.id = a.survey_id
                        where c.state = 'done' and a.suggested_answer_id is not null
                        and i.id = 1
                        and ss.periode = '"""+periode+"""'
                        GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                        ORDER BY a.question_id ASC
                    ) AS subq
                    GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                    ORDER BY subq.survey_name
                )
                UNION ALL
                select
                    'max-03' as survey_key,
                    'MAX' as survey_name,
                    'MAX' as jenis_industri,
                    5 AS parameter_1,
                    5 AS parameter_2,
                    5 AS parameter_3
                       """
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/chart3', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _chart3(self, **kwargs):
        survey_id = kwargs.get('survey_id')
        periode = kwargs.get('periode')
        jenis_industri = kwargs.get('jenis_industri')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Efektivitas fungsi pengelola risiko%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Tingkat kematangan organ pengelola%' THEN subq.avg END), 2) AS parameter_2,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Keterlibatan aktif Dewan Komisaris/ Dewan%' THEN subq.avg END), 2) AS parameter_3,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Eskalasi permasalahan kepada Dewan Komisaris%' THEN subq.avg END), 2) AS parameter_4,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Tingkat pemahaman Risiko di jajaran Dewan Komisaris%' THEN subq.avg END), 2) AS parameter_5,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Peran komite komite di bawah Dewan Komisaris/%' THEN subq.avg END), 2) AS parameter_6,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Pengurusan aktif Direksi dalam pengelolaan Risiko%' THEN subq.avg END), 2) AS parameter_7,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Mandat, wewenang, dan independensi fungsi Manajemen%' THEN subq.avg END), 2) AS parameter_8,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Efektivitas fungsi pengelola risiko dalam%' THEN subq.avg END), 2) AS parameter_9,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Penerapan Model Tata Kelola Risiko Tiga Lini%' THEN subq.avg END), 2) AS parameter_10,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Pertama%' THEN subq.avg END), 2) AS parameter_11,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Kedua%' THEN subq.avg END), 2) AS parameter_12,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Ketiga%' THEN subq.avg END), 2) AS parameter_13,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Interaksi antara fungsi Risiko dan Assurance%' THEN subq.avg END), 2) AS parameter_14,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Peran dan fungsi Tata Kelola Risiko Terintegrasi%' THEN subq.avg END), 2) AS parameter_15,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Monitoring risiko entitas induk sampai ke entitas anak%' THEN subq.avg END), 2) AS parameter_16
                        FROM (
                            select
                            'sur-' || CAST(ss.id as TEXT) as survey_key,
                            (ss.title->>'en_US')::varchar AS survey_name,
                            ss.jenis_industri,
                            (b.title->>'en_US')::varchar AS parameter,
                            ROUND(MIN((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where a.survey_id = """+survey_id+""" and c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 2
                            and ss.periode = '"""+periode+"""'
                            GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id, ss.title, h.name, ss.id, b.title
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Efektivitas fungsi pengelola risiko%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Tingkat kematangan organ pengelola%' THEN subq.avg END), 2) AS parameter_2,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Keterlibatan aktif Dewan Komisaris/ Dewan%' THEN subq.avg END), 2) AS parameter_3,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Eskalasi permasalahan kepada Dewan Komisaris%' THEN subq.avg END), 2) AS parameter_4,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Tingkat pemahaman Risiko di jajaran Dewan Komisaris%' THEN subq.avg END), 2) AS parameter_5,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran komite komite di bawah Dewan Komisaris/%' THEN subq.avg END), 2) AS parameter_6,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Pengurusan aktif Direksi dalam pengelolaan Risiko%' THEN subq.avg END), 2) AS parameter_7,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Mandat, wewenang, dan independensi fungsi Manajemen%' THEN subq.avg END), 2) AS parameter_8,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Efektivitas fungsi pengelola risiko dalam%' THEN subq.avg END), 2) AS parameter_9,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Penerapan Model Tata Kelola Risiko Tiga Lini%' THEN subq.avg END), 2) AS parameter_10,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Pertama%' THEN subq.avg END), 2) AS parameter_11,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Kedua%' THEN subq.avg END), 2) AS parameter_12,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Ketiga%' THEN subq.avg END), 2) AS parameter_13,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Interaksi antara fungsi Risiko dan Assurance%' THEN subq.avg END), 2) AS parameter_14,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Tata Kelola Risiko Terintegrasi%' THEN subq.avg END), 2) AS parameter_15,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Monitoring risiko entitas induk sampai ke entitas anak%' THEN subq.avg END), 2) AS parameter_16
                        FROM (
                            select
                            'max-01'as survey_key,
                            'MAX INDUSTRI """+jenis_industri+"""' AS survey_name,
                            (b.title->>'en_US')::varchar AS parameter,
                            'MAX """+jenis_industri+"""' as jenis_industri,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 2
                            and ss.periode = '"""+periode+"""'
                            and ss.jenis_industri = '"""+jenis_industri+"""'
                            GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Efektivitas fungsi pengelola risiko%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Tingkat kematangan organ pengelola%' THEN subq.avg END), 2) AS parameter_2,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Keterlibatan aktif Dewan Komisaris/ Dewan%' THEN subq.avg END), 2) AS parameter_3,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Eskalasi permasalahan kepada Dewan Komisaris%' THEN subq.avg END), 2) AS parameter_4,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Tingkat pemahaman Risiko di jajaran Dewan Komisaris%' THEN subq.avg END), 2) AS parameter_5,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran komite komite di bawah Dewan Komisaris/%' THEN subq.avg END), 2) AS parameter_6,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Pengurusan aktif Direksi dalam pengelolaan Risiko%' THEN subq.avg END), 2) AS parameter_7,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Mandat, wewenang, dan independensi fungsi Manajemen%' THEN subq.avg END), 2) AS parameter_8,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Efektivitas fungsi pengelola risiko dalam%' THEN subq.avg END), 2) AS parameter_9,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Penerapan Model Tata Kelola Risiko Tiga Lini%' THEN subq.avg END), 2) AS parameter_10,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Pertama%' THEN subq.avg END), 2) AS parameter_11,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Kedua%' THEN subq.avg END), 2) AS parameter_12,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Lini Ketiga%' THEN subq.avg END), 2) AS parameter_13,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Interaksi antara fungsi Risiko dan Assurance%' THEN subq.avg END), 2) AS parameter_14,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Peran dan fungsi Tata Kelola Risiko Terintegrasi%' THEN subq.avg END), 2) AS parameter_15,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Monitoring risiko entitas induk sampai ke entitas anak%' THEN subq.avg END), 2) AS parameter_16
                        FROM (
                            select
                            'max-01'as survey_key,
                            'MAX ALL DATA' AS survey_name,
                            (b.title->>'en_US')::varchar AS parameter,
                            'MAX ALL DATA' as jenis_industri,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 2
                            and ss.periode = '"""+periode+"""'
                            GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    select
                        'max-03' as survey_key,
                        'MAX' as survey_name,
                        'MAX' as jenis_industri,
                        5 AS parameter_1,
                        5 AS parameter_2,
                        5 AS parameter_3,
                        5 AS parameter_4,
                        5 AS parameter_5,
                        5 AS parameter_6,
                        5 AS parameter_7,
                        5 AS parameter_8,
                        5 AS parameter_9,
                        5 AS parameter_10,
                        5 AS parameter_11,
                        5 AS parameter_12,
                        5 AS parameter_13,
                        5 AS parameter_14,
                        5 AS parameter_15,
                        5 AS parameter_16
                           """
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/chart4', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _chart4(self, **kwargs):
        survey_id = kwargs.get('survey_id')
        periode = kwargs.get('periode')
        jenis_industri = kwargs.get('jenis_industri')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                        (
                            SELECT
                                subq.survey_key,
                                subq.survey_name,
                                subq.jenis_industri,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Peningkatan kualitas kerangka Manajemen Risiko%' THEN subq.avg END), 2) AS parameter_1,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Rencana transformasi Enterprise Risk Management%' THEN subq.avg END), 2) AS parameter_2,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Peran Manajemen Risiko dalam penyusunan rencana%' THEN subq.avg END), 2) AS parameter_3,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Hubungan peran Manajemen Risiko terhadap pencapaian%' THEN subq.avg END), 2) AS parameter_4,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Kapasitas risiko%' THEN subq.avg END), 2) AS parameter_5,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Selera Risiko%' THEN subq.avg END), 2) AS parameter_6,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Komunikasi selera Risiko kepada pemangku%' THEN subq.avg END), 2) AS parameter_7,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Kebijakan Risiko%' THEN subq.avg END), 2) AS parameter_8,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Prosedur risiko%' THEN subq.avg END), 2) AS parameter_9,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Rencana darurat (contingency plan) dalam kondisi%' THEN subq.avg END), 2) AS parameter_10,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Reviu dan Stress test terhadap prosedur dan SOP%' THEN subq.avg END), 2) AS parameter_11,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Organ fungsi kepatuhan dan perannya%' THEN subq.avg END), 2) AS parameter_12,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Penerapan Kerangka Integrated Enterprise Risk Management (ERM)%' THEN subq.avg END), 2) AS parameter_13,
                                ROUND(AVG(CASE WHEN subq.parameter like '%Efektivitas Pengendalian Intern%' THEN subq.avg END), 2) AS parameter_14
                            FROM (
                                select
                                'sur-' || CAST(ss.id as TEXT) as survey_key,
                                (ss.title->>'en_US')::varchar AS survey_name,
                                ss.jenis_industri,
                                (b.title->>'en_US')::varchar AS parameter,
                                ROUND(MIN((e.value->>'en_US')::int), 2) AS avg
                                from survey_user_input_line as a
                                left join survey_question as b on a.question_id = b.id
                                left join survey_user_input as c on c.id = a.user_input_id
                                left join res_partner as d on d.id = c.partner_id
                                left join survey_question_answer as e on e.id = a.suggested_answer_id
                                left join res_users as f on f.partner_id = d.id
                                left join hr_employee as g on g.user_id = f.id
                                left join res_company as h on h.id = g.company_id
                                left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                left join survey_survey as ss on ss.id = a.survey_id
                                where a.survey_id = """+survey_id+""" and c.state = 'done' and a.suggested_answer_id is not null
                                and i.id = 3
                                and ss.periode = '"""+periode+"""'
                                GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id, ss.title, h.name, ss.id, b.title
                                ORDER BY a.question_id ASC
                            ) AS subq
                            GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                            ORDER BY subq.survey_name
                        )
                        UNION ALL
                        (
                            SELECT
                                subq.survey_key,
                                subq.survey_name,
                                subq.jenis_industri,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Peningkatan kualitas kerangka Manajemen Risiko%' THEN subq.avg END), 2) AS parameter_1,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Rencana transformasi Enterprise Risk Management%' THEN subq.avg END), 2) AS parameter_2,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Peran Manajemen Risiko dalam penyusunan rencana%' THEN subq.avg END), 2) AS parameter_3,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Hubungan peran Manajemen Risiko terhadap pencapaian%' THEN subq.avg END), 2) AS parameter_4,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Kapasitas risiko%' THEN subq.avg END), 2) AS parameter_5,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Selera Risiko%' THEN subq.avg END), 2) AS parameter_6,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Komunikasi selera Risiko kepada pemangku%' THEN subq.avg END), 2) AS parameter_7,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Kebijakan Risiko%' THEN subq.avg END), 2) AS parameter_8,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Prosedur risiko%' THEN subq.avg END), 2) AS parameter_9,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Rencana darurat (contingency plan) dalam kondisi%' THEN subq.avg END), 2) AS parameter_10,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Reviu dan Stress test terhadap prosedur dan SOP%' THEN subq.avg END), 2) AS parameter_11,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Organ fungsi kepatuhan dan perannya%' THEN subq.avg END), 2) AS parameter_12,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Penerapan Kerangka Integrated Enterprise Risk Management (ERM)%' THEN subq.avg END), 2) AS parameter_13,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Efektivitas Pengendalian Intern%' THEN subq.avg END), 2) AS parameter_14
                            FROM (
                                select
                                'max-01'as survey_key,
                                'MAX INDUSTRI """+jenis_industri+"""' AS survey_name,
                                (b.title->>'en_US')::varchar AS parameter,
                                'MAX """+jenis_industri+"""' as jenis_industri,
                                ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                                from survey_user_input_line as a
                                left join survey_question as b on a.question_id = b.id
                                left join survey_user_input as c on c.id = a.user_input_id
                                left join res_partner as d on d.id = c.partner_id
                                left join survey_question_answer as e on e.id = a.suggested_answer_id
                                left join res_users as f on f.partner_id = d.id
                                left join hr_employee as g on g.user_id = f.id
                                left join res_company as h on h.id = g.company_id
                                left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                left join survey_survey as ss on ss.id = a.survey_id
                                where c.state = 'done' and a.suggested_answer_id is not null
                                and i.id = 3
                                and ss.periode = '"""+periode+"""'
                                and ss.jenis_industri = '"""+jenis_industri+"""'
                                GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                                ORDER BY a.question_id ASC
                            ) AS subq
                            GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                            ORDER BY subq.survey_name
                        )
                        UNION ALL
                        (
                            SELECT
                                subq.survey_key,
                                subq.survey_name,
                                subq.jenis_industri,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Peningkatan kualitas kerangka Manajemen Risiko%' THEN subq.avg END), 2) AS parameter_1,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Rencana transformasi Enterprise Risk Management%' THEN subq.avg END), 2) AS parameter_2,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Peran Manajemen Risiko dalam penyusunan rencana%' THEN subq.avg END), 2) AS parameter_3,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Hubungan peran Manajemen Risiko terhadap pencapaian%' THEN subq.avg END), 2) AS parameter_4,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Kapasitas risiko%' THEN subq.avg END), 2) AS parameter_5,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Selera Risiko%' THEN subq.avg END), 2) AS parameter_6,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Komunikasi selera Risiko kepada pemangku%' THEN subq.avg END), 2) AS parameter_7,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Kebijakan Risiko%' THEN subq.avg END), 2) AS parameter_8,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Prosedur risiko%' THEN subq.avg END), 2) AS parameter_9,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Rencana darurat (contingency plan) dalam kondisi%' THEN subq.avg END), 2) AS parameter_10,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Reviu dan Stress test terhadap prosedur dan SOP%' THEN subq.avg END), 2) AS parameter_11,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Organ fungsi kepatuhan dan perannya%' THEN subq.avg END), 2) AS parameter_12,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Penerapan Kerangka Integrated Enterprise Risk Management (ERM)%' THEN subq.avg END), 2) AS parameter_13,
                                ROUND(MAX(CASE WHEN subq.parameter like '%Efektivitas Pengendalian Intern%' THEN subq.avg END), 2) AS parameter_14
                            FROM (
                                select
                                'max-01'as survey_key,
                                'MAX ALL DATA' AS survey_name,
                                (b.title->>'en_US')::varchar AS parameter,
                                'MAX ALL DATA' as jenis_industri,
                                ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                                from survey_user_input_line as a
                                left join survey_question as b on a.question_id = b.id
                                left join survey_user_input as c on c.id = a.user_input_id
                                left join res_partner as d on d.id = c.partner_id
                                left join survey_question_answer as e on e.id = a.suggested_answer_id
                                left join res_users as f on f.partner_id = d.id
                                left join hr_employee as g on g.user_id = f.id
                                left join res_company as h on h.id = g.company_id
                                left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                left join survey_survey as ss on ss.id = a.survey_id
                                where c.state = 'done' and a.suggested_answer_id is not null
                                and i.id = 3
                                and ss.periode = '"""+periode+"""'
                                GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                                ORDER BY a.question_id ASC
                            ) AS subq
                            GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                            ORDER BY subq.survey_name
                        )
                        UNION ALL
                        select
                            'max-03' as survey_key,
                            'MAX' as survey_name,
                            'MAX' as jenis_industri,
                            5 AS parameter_1,
                            5 AS parameter_2,
                            5 AS parameter_3,
                            5 AS parameter_4,
                            5 AS parameter_5,
                            5 AS parameter_6,
                            5 AS parameter_7,
                            5 AS parameter_8,
                            5 AS parameter_9,
                            5 AS parameter_10,
                            5 AS parameter_11,
                            5 AS parameter_12,
                            5 AS parameter_13,
                            5 AS parameter_14
                               """
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/chart5', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _chart5(self, **kwargs):
        survey_id = kwargs.get('survey_id')
        periode = kwargs.get('periode')
        jenis_industri = kwargs.get('jenis_industri')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Identifikasi Risiko utama%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Pengukuran Risiko%' THEN subq.avg END), 2) AS parameter_2,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Kerangka proses pengukuran Risiko untuk prioritisasi Risiko%' THEN subq.avg END), 2) AS parameter_3,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Integrasi atas seluruh Risiko utama%' THEN subq.avg END), 2) AS parameter_4,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Aktivitas perlakuan terhadap Risiko utama%' THEN subq.avg END), 2) AS parameter_5,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Identifikasi dan pengelolaan eksposur Risiko yang berada diatas selera risiko%' THEN subq.avg END), 2) AS parameter_6,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Pelaporan Risiko melaporkan Risiko secara real-time%' THEN subq.avg END), 2) AS parameter_7
                        FROM (
                            select
                            'sur-' || CAST(ss.id as TEXT) as survey_key,
                            (ss.title->>'en_US')::varchar AS survey_name,
                            ss.jenis_industri,
                            (b.title->>'en_US')::varchar AS parameter,
                            ROUND(MIN((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where a.survey_id = """+survey_id+""" and c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 4
                            and ss.periode = '"""+periode+"""'
                            GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id, ss.title, h.name, ss.id, b.title
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Identifikasi Risiko utama%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Pengukuran Risiko%' THEN subq.avg END), 2) AS parameter_2,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Kerangka proses pengukuran Risiko untuk prioritisasi Risiko%' THEN subq.avg END), 2) AS parameter_3,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Integrasi atas seluruh Risiko utama%' THEN subq.avg END), 2) AS parameter_4,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Aktivitas perlakuan terhadap Risiko utama%' THEN subq.avg END), 2) AS parameter_5,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Identifikasi dan pengelolaan eksposur Risiko yang berada diatas selera risiko%' THEN subq.avg END), 2) AS parameter_6,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Pelaporan Risiko melaporkan Risiko secara real-time%' THEN subq.avg END), 2) AS parameter_7
                        FROM (
                            select
                            'max-01'as survey_key,
                            'MAX INDUSTRI """+jenis_industri+"""' AS survey_name,
                            (b.title->>'en_US')::varchar AS parameter,
                            'MAX """+jenis_industri+"""' as jenis_industri,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 4
                            and ss.periode = '"""+periode+"""'
                            and ss.jenis_industri = '"""+jenis_industri+"""'
                            GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Identifikasi Risiko utama%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Pengukuran Risiko%' THEN subq.avg END), 2) AS parameter_2,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Kerangka proses pengukuran Risiko untuk prioritisasi Risiko%' THEN subq.avg END), 2) AS parameter_3,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Integrasi atas seluruh Risiko utama%' THEN subq.avg END), 2) AS parameter_4,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Aktivitas perlakuan terhadap Risiko utama%' THEN subq.avg END), 2) AS parameter_5,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Identifikasi dan pengelolaan eksposur Risiko yang berada diatas selera risiko%' THEN subq.avg END), 2) AS parameter_6,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Pelaporan Risiko melaporkan Risiko secara real-time%' THEN subq.avg END), 2) AS parameter_7
                        FROM (
                            select
                            'max-01'as survey_key,
                            'MAX ALL DATA' AS survey_name,
                            (b.title->>'en_US')::varchar AS parameter,
                            'MAX ALL DATA' as jenis_industri,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 4
                            and ss.periode = '"""+periode+"""'
                            GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    select
                        'max-03' as survey_key,
                        'MAX' as survey_name,
                        'MAX' as jenis_industri,
                        5 AS parameter_1,
                        5 AS parameter_2,
                        5 AS parameter_3,
                        5 AS parameter_4,
                        5 AS parameter_5,
                        5 AS parameter_6,
                        5 AS parameter_7
                                   """
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/chart6', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _chart6(self, **kwargs):
        survey_id = kwargs.get('survey_id')
        periode = kwargs.get('periode')
        jenis_industri = kwargs.get('jenis_industri')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Data Risiko%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(AVG(CASE WHEN subq.parameter like '%Permodelan dan Teknologi Risiko%' THEN subq.avg END), 2) AS parameter_2
                        FROM (
                            select
                            'sur-' || CAST(ss.id as TEXT) as survey_key,
                            (ss.title->>'en_US')::varchar AS survey_name,
                            ss.jenis_industri,
                            (b.title->>'en_US')::varchar AS parameter,
                            ROUND(MIN((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where a.survey_id = """+survey_id+""" and c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 5
                            and ss.periode = '"""+periode+"""'
                            GROUP BY a.question_id, i.name, j.name, a.survey_id, j.id, i.id, ss.title, h.name, ss.id, b.title
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Data Risiko%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Permodelan dan Teknologi Risiko%' THEN subq.avg END), 2) AS parameter_2
                        FROM (
                            select
                            'max-01'as survey_key,
                            'MAX INDUSTRI """+jenis_industri+"""' AS survey_name,
                            (b.title->>'en_US')::varchar AS parameter,
                            'MAX """+jenis_industri+"""' as jenis_industri,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 5
                            and ss.periode = '"""+periode+"""'
                            and ss.jenis_industri = '"""+jenis_industri+"""'
                            GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    (
                        SELECT
                            subq.survey_key,
                            subq.survey_name,
                            subq.jenis_industri,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Data Risiko%' THEN subq.avg END), 2) AS parameter_1,
                            ROUND(MAX(CASE WHEN subq.parameter like '%Permodelan dan Teknologi Risiko%' THEN subq.avg END), 2) AS parameter_2
                        FROM (
                            select
                            'max-01'as survey_key,
                            'MAX ALL DATA' AS survey_name,
                            (b.title->>'en_US')::varchar AS parameter,
                            'MAX ALL DATA' as jenis_industri,
                            ROUND(MAX((e.value->>'en_US')::int), 2) AS avg
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join res_users as f on f.partner_id = d.id
                            left join hr_employee as g on g.user_id = f.id
                            left join res_company as h on h.id = g.company_id
                            left join rmi_param_dimensi as i on i.id = b.dimensi_names
                            left join rmi_param_group as j on j.id = b.sub_dimensi_names
                            left join survey_survey as ss on ss.id = a.survey_id
                            where c.state = 'done' and a.suggested_answer_id is not null
                            and i.id = 5
                            and ss.periode = '"""+periode+"""'
                            GROUP BY a.question_id, parameter, i.name, j.name, survey_name, a.survey_id, ss.id
                            ORDER BY a.question_id ASC
                        ) AS subq
                        GROUP BY subq.survey_name, subq.jenis_industri, subq.survey_key
                        ORDER BY subq.survey_name
                    )
                    UNION ALL
                    select
                        'max-03' as survey_key,
                        'MAX' as survey_name,
                        'MAX' as jenis_industri,
                        5 AS parameter_1,
                        5 AS parameter_2
                                       """
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/ofi', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _ofi(self, **kwargs):
        survey_id = kwargs.get('survey_id')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not survey_id:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "survey_id" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                     select
                        ROW_NUMBER() OVER () AS no,
                         a.survey_id,
                        (ss.title->>'en_US')::varchar AS survey_name,
                        ss.periode,
                        ss.jenis_industri,
                        i.id as dimensi_id,
                        i.name as dimensi,
                        j.name as subdimensi,
                        (b.title->>'en_US')::varchar AS parameterName,
                        min((e.value->>'en_US')::int) as minvalue
                        from survey_user_input_line as a
                        left join survey_question as b on a.question_id = b.id
                        left join survey_user_input as c on c.id = a.user_input_id
                        left join res_partner as d on d.id = c.partner_id
                        left join survey_question_answer as e on e.id = a.suggested_answer_id
                        left join res_users as f on f.partner_id = d.id
                        left join hr_employee as g on g.user_id = f.id
                        left join res_company as h on h.id = g.company_id
                        left join rmi_param_dimensi as i on i.id = b.dimensi_names
                        left join rmi_param_group as j on j.id = b.sub_dimensi_names
                        left join survey_survey as ss on ss.id = a.survey_id
                    where a.survey_id = """+survey_id+""" and c.state = 'done' and a.suggested_answer_id is not null
                    GROUP BY b.id, parameterName, i.name, j.name, survey_name, a.survey_id, dimensi_id, ss.periode,ss.jenis_industri
                    ORDER BY b.id ASC"""
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/ofi-detail', website=False, auth='public', type="http", csrf=False, methods=['GET'])
    def _ofi_detail(self, **kwargs):
        paramter_name = kwargs.get('paramter_name')
        level = kwargs.get('level')
        jenis_industri = kwargs.get('jenis_industri')
        data = []
        body = {}
        statusCode = 200
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        try:
            query = """
                 select
                    ROW_NUMBER() OVER () AS no,
                    *
                from x_master_parameter
                where
                    parameter_name like '%"""+paramter_name+"""%'
                    and level = """+level+"""
                    and jenisindustri = '"""+jenis_industri+"""'"""
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)

    @http.route('/api/report/all-survey-data', website=False, auth='public', type="http", csrf=False,
                methods=['GET'])
    def _all_survey_data(self, **kwargs):
        periode = kwargs.get('periode')
        data = []
        origin = http.request.httprequest.headers.get('Origin')
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true'
        }
        if not periode:
            statusCode = 400
            body = {
                'status': False,
                'message': 'Required parameter "periode" is missing'
            }
            return Response(json.dumps(body), headers=headers, status=statusCode)
        try:
            query = """
                      select
                        ROW_NUMBER() OVER () AS no,
                        sub.survey_id,
                        sub.survey_name,
                        sub.question_id,
                        sub.company,
                        sub.jenis_industri,
                        sub.periode,
                        sub.dimensi_id,
                        sub.dimensi,
                        sub.subdimensi_id,
                        sub.subdimensi,
                        sub.parameter_id,
                        sub.parameter,
                        sub.user,
                        sub.Department,
                        sub.answer
                        from (
                            select
                                (ss.title->>'en_US')::varchar AS survey_name,
                                a.question_id ,
                                a.survey_id,
                                h.name as company,
                                ss.jenis_industri,
                                ss.periode,
                                i.name as dimensi,
                                i.id as dimensi_id,
                                j.name as subdimensi,
                                j.id as subdimensi_id,
                                (b.title->>'en_US')::varchar AS parameter,
                                b.id as parameter_id,
                                d.name as "user",
                                hr.name as Department,
                                (e.value->>'en_US')::int AS answer
                                from survey_user_input_line as a
                                left join survey_question as b on a.question_id = b.id
                                left join survey_user_input as c on c.id = a.user_input_id
                                left join res_partner as d on d.id = c.partner_id
                                left join survey_question_answer as e on e.id = a.suggested_answer_id
                                left join res_users as f on f.partner_id = d.id
                                left join hr_employee as g on g.user_id = f.id
                                left join res_company as h on h.id = g.company_id
                                left join rmi_param_dimensi as i on i.id = b.dimensi_names
                                left join rmi_param_group as j on j.id = b.sub_dimensi_names
                                left join survey_survey as ss on ss.id = a.survey_id
                                left join hr_department as hr on hr.id = g.department_id
                                left join survey_user_input_line as sqa on sqa.question_id = a.question_id and sqa.suggested_answer_id is null and sqa.write_uid = f.id
                                where
                                    c.state = 'done' and a.suggested_answer_id is not null and ss.periode = '"""+periode+"""'
                                order by survey_id, d.company_id, question_id
                    ) as sub"""
            http.request.env.cr.execute(query)
            fetched_data = http.request.env.cr.fetchall()
            column_names = [desc[0] for desc in http.request.env.cr.description]
            for row in fetched_data:
                row_dict = dict(zip(column_names, row))
                for key, value in row_dict.items():
                    if isinstance(value, datetime):
                        row_dict[key] = str(value)
                data.append(row_dict)
            body = {'status': True, 'message': 'OK', 'data': data}
            statusCode = 200
        except Exception as e:
            errorMsg = f"An error occurred: {e}"
            body = {
                'status': False,
                'message': errorMsg,
                'execution_time': '0s'
            }
            statusCode = 500
        return Response(json.dumps(body), headers=headers, status=statusCode)