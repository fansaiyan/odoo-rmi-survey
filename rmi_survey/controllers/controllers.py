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
                        max((e.value->>'en_US')::int) - min((e.value->>'en_US')::int) as rangevalue
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
                    where a.survey_id = {} and c.state = 'done'
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
                where a.survey_id = {} and c.state = 'done' and a.question_id = {}
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
    @http.route('/api/aspek-dimensi-corporate', website=False, auth='public', type="http", csrf=False, methods=['GET'])
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
                        CASE
                            WHEN f.name = 'Budaya dan Kapabilitas Risiko' THEN '1 s.d. 3'
                            WHEN f.name = 'Organisasi dan Tata Kelola Risiko' THEN '4 s.d. 19'
                            WHEN f.name = 'Kerangka Risiko dan Kepatuhan' THEN '20 s.d. 33'
                            WHEN f.name = 'Proses dan Kontrol Risiko' THEN '34 s.d. 39'
                            ELSE '40 s.d. 42'
                        END as parameter,
                        f.param_dimensi_id AS dimensi,
                        f.name as deskripsi,
                        TRUNC(avg((e.value->>'en_US')::int) * 10) / 10.0 AS skordimensi
                        from survey_user_input_line as a
                        left join survey_question as b on a.question_id = b.id
                        left join survey_user_input as c on c.id = a.user_input_id
                        left join res_partner as d on d.id = c.partner_id
                        left join survey_question_answer as e on e.id = a.suggested_answer_id
                        left join rmi_param_dimensi as f on f.id = b.dimensi_names
                        left join rmi_param_group as g on g.id = b.sub_dimensi_names
                    where a.survey_id = {}
                    group by f.name, f.id
                    order by f.id asc
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
                            CASE
                                WHEN f.name = 'Budaya dan Kapabilitas Risiko' THEN '1 s.d. 3'
                                WHEN f.name = 'Organisasi dan Tata Kelola Risiko' THEN '4 s.d. 19'
                                WHEN f.name = 'Kerangka Risiko dan Kepatuhan' THEN '20 s.d. 33'
                                WHEN f.name = 'Proses dan Kontrol Risiko' THEN '34 s.d. 39'
                                ELSE '40 s.d. 42'
                            END as parameter,
                            f.param_dimensi_id AS dimensi,
                            f.name as deskripsi,
                            TRUNC(avg((e.value->>'en_US')::int) * 10) / 10.0 AS skordimensi
                            from survey_user_input_line as a
                            left join survey_question as b on a.question_id = b.id
                            left join survey_user_input as c on c.id = a.user_input_id
                            left join res_partner as d on d.id = c.partner_id
                            left join survey_question_answer as e on e.id = a.suggested_answer_id
                            left join rmi_param_dimensi as f on f.id = b.dimensi_names
                            left join rmi_param_group as g on g.id = b.sub_dimensi_names
                        where a.survey_id = {}
                        group by f.name, f.id
                        order by f.id asc
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