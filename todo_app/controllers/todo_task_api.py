import math
from odoo import http
from odoo.http import request
from urllib.parse import parse_qs
import json


def invalid_response(error , status):
    response_body={
       'error' : error
    }
    return request.make_json_response(response_body , status=status)

def valid_response(data , status , pagination_info):
    response_body={
       'data' : data ,
       'massage':'success'
    }
    if pagination_info :
        response_body['pagination_info']=pagination_info
    return request.make_json_response(response_body , status=status)


class TodoTaskController(http.Controller):

    @http.route('/api/task', methods=['POST'], type='http', auth='none', csrf=False)
    def create_task(self):
        args=request.httprequest.data.decode()
        vals=json.loads(args)
        res=request.env['todo.task'].sudo().create(vals)

        if not vals.get('name'):
            return request.make_json_response({
                "massage": "Name is required!",
            }, status=400)
        try:
            if res:
                return request.make_json_response({
                    "massage":"task has been created successfuly",
                    "id":res.id,
                    "name":res.name
                },status=201)
        except Exception as error:
            return request.make_json_response({
                "massage": error,
            }, status=400)

    @http.route('/api/task/<int:task_id>', methods=['PUT'], type='http', auth='none', csrf=False)
    def update_task(self,task_id):
        try:
            task_id = request.env['todo.task'].sudo().search([('id','=',task_id)])
            if not task_id:
                return request.make_json_response({
                    "massage": "ID does not exist!",
                }, status=400)
            args = request.httprequest.data.decode()
            vals = json.loads(args)
            task_id.write(vals)
            return request.make_json_response({
                "massage": "task has been created successfuly",
                "id": task_id.id,
                "name": task_id.name
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "massage": error,
            }, status=400)

    @http.route('/api/task/<int:task_id>', methods=['GET'], type='http', auth='none', csrf=False)
    def get_task(self, task_id):
        try:
            task_id = request.env['todo.task'].sudo().search([('id', '=', task_id)])
            if not task_id:
                return request.make_json_response({
                    "massage": "ID does not exist!",
                }, status=400)

            return request.make_json_response({
                "id": task_id.id,
                "name": task_id.name
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route('/api/task/<int:task_id>', methods=['DELETE'], type='http', auth='none', csrf=False)
    def delete_task(self, task_id):
        try:
            task_id = request.env['todo.task'].sudo().search([('id', '=', task_id)])
            if not task_id:
                return request.make_json_response({
                    "massage": "ID does not exist!",
                }, status=400)

            task_id.unlink()
            return request.make_json_response({
                "massage": "Task has been deleted successfully"
            }, status=200)

        except Exception as error:
            return request.make_json_response({
                "error": error,
            }, status=400)

    @http.route('/api/tasks', methods=['GET'], type='http', auth='none', csrf=False)
    def get_task_list(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            task_domin = []
            page = offset = None
            limit  = 5

            if params:
                if params.get('limit'):
                    limit = int(params.get('limit')[0])
                if params.get('page'):
                    page = int(params.get('page')[0])

            if page:
                offset = (page*limit)-limit

            if params.get('status'):
                task_domin += [('status','=',params.get('status')[0])]

            task_ids = request.env['todo.task'].sudo().search(task_domin,offset=offset ,limit=limit , order='id DESC')
            task_count = request.env['todo.task'].sudo().search_count(task_domin)

            if not task_ids:
                return invalid_response( "There are not records!", status=400)

            return valid_response([{
                "id": task_id.id,
                "name": task_id.name,
                "status": task_id.status
            }for task_id in task_ids], pagination_info={
                'page': page if page else 1,
                'limit':limit ,
                'pages':math.ceil(task_count/limit) if limit else 1,
                'count':task_count
            } , status=200)

        except Exception as error:
            return invalid_response(error, status=400)