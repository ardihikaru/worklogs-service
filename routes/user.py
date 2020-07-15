"""
    List of routes for /api/users* endpoints
"""

from aiohttp_route_decorator import RouteCollector
import aiohttp
from controllers.user.user import User
from addons.utils import get_unprocessable_request

route = RouteCollector()


@route('', methods=['POST', 'GET', 'PUT', 'DELETE'])
async def index(request):
    """
        Endpoint to:
         1. POST new user data
            Try: curl http://localhost:8080/api/users -X POST -H "Content-Type: application/json"
                    -d '{
                            "name": "Muhammad Febrian Ardiansyah",
                            "username": "ardihikaru",
                            "email": "ardihikaru3@gmail.com",
                            "password": "ardipasswd",
                            "password_confirm": "ardipasswd"
                    }'
         1. GET all user data
            Try: curl http://localhost:8080/api/users
         1. PUT (update) a specific user data
            Try: curl http://localhost:8080/api/users -X POST -H "Content-Type: application/json"
                    -d '{
                            "_id": {String},
                            "name": "Muhammad Febrian Ardiansyah",
                    }'
         1. DELETE a specific user data (single ID)
            Try: curl http://localhost:8080/api/users -X DELETE -H "Content-Type: application/json"
                    -d '{
                            "_id": {String}
                    }'
         2. DELETE list of user data (multiple IDs)
            Try: curl http://localhost:8080/api/users -X DELETE -H "Content-Type: application/json"
                    -d '{
                            "_id": [{String}, {String}]
                    }'
    """

    if request.method == 'POST':
        try:
            json_data = await request.json()
            resp = User().register(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)

    if request.method == 'GET':
        resp = User().get_users()
        return aiohttp.web.json_response(resp)

    if request.method == 'PUT':
        try:
            json_data = await request.json()
            resp = User().update_data_by_id(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)

    if request.method == 'DELETE':
        try:
            json_data = await request.json()
            resp = User().delete_data_by_id(json_data)
        except:
            return get_unprocessable_request()

        return aiohttp.web.json_response(resp)
