"""
    List of routes for /api/worklogs* endpoints
"""

from aiohttp_route_decorator import RouteCollector
import aiohttp
from controllers.work_logs.work_logs import WorkLogs as DataController
from addons.utils import get_unprocessable_request

route = RouteCollector()


@route('', methods=['POST', 'GET'])
async def index(request):
    """
        Endpoint to:
         1. GET all worklogs data
            Try: curl http://localhost:8080/api/worklogs
         2. POST a new worklogs data
            Try: curl http://localhost:8080/api/worklogs -X POST -H "Content-Type: application/json"
                    -d '{
                            "task": "Initial Meeting",
                            "description": "Scrum meeting & Introduction",
                            "work_datetime": "2020-07-15 02:42:02",
                            "work_hours": 6
                        }'
    """

    if request.method == 'POST':
        try:
            json_data = await request.json()
            print(" --- json_data:", json_data)
            resp = DataController().register(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)

    if request.method == 'GET':
        resp = DataController().get_data()
        return aiohttp.web.json_response(resp)


@route('/{_id}', methods=['GET', 'DELETE', 'PUT'])
async def index_by(request):
    """
        Endpoint to:
         1. GET worklogs data by id
            Try: curl http://localhost:8080/api/worklogs/{_id}
         2. DELETE worklogs data by id
            Try: curl http://localhost:8080/api/worklogs/{_id} -X DELETE
         3. PUT (Edit) worklogs data by id
            Try: curl http://localhost:8080/api/worklogs/{_id}
                    -X POST -H "Content-Type: application/json" -d '{"currency":"EUR"}'
    """


    try:
        _id = str(request.match_info['_id'])
    except:
        return get_unprocessable_request()

    if request.method == 'GET':
        resp = DataController().get_data_by_id(_id)
        return aiohttp.web.json_response(resp)
    elif request.method == 'DELETE':
        resp = DataController().delete_data_by_id(_id)
        return aiohttp.web.json_response(resp)
    elif request.method == 'PUT':
        try:
            json_data = await request.json()
            resp = DataController().update_data_by_id(_id, json_data)
            return aiohttp.web.json_response(resp)
        except:
            return get_unprocessable_request()
    else:
        return get_unprocessable_request()
