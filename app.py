import asab
import asab.web
import asab.web.rest
import asab.web.session
from routes import auth as route_auth
from routes import user as route_user
from aiohttp_jwt import JWTMiddleware
from mongoengine import connect
from addons.database_blacklist.blacklist_helpers import is_token_revoked
from addons.redis.my_redis import MyRedis


class WebService(asab.Application):
    async def initialize(self):
        # Connect Database
        connect('WorkLogs')

        # Loading the web service module
        self.add_module(asab.web.Module)

        # Locate web service
        websvc = self.get_service("asab.WebService")

        # Create a dedicated web container
        container = asab.web.WebContainer(websvc, 'webservice:yawes')

        # Config routes
        route_auth.route.add_to_router(container.WebApp.router, prefix='/api/auth')
        route_user.route.add_to_router(container.WebApp.router, prefix='/api/users')

        # Enable exception to JSON exception middleware
        container.WebApp.middlewares.append(asab.web.rest.JsonExceptionMiddleware)

        # Enable exception to JWT middleware
        container.WebApp.middlewares.append(JWTMiddleware(
            secret_or_pub_key=asab.Config["jwt"]["secret_key"],
            request_property="user",
            whitelist=[r"/api/users*", r"/api/auth/login"],  # use this to disable access_token validation
            # whitelist=[r"/api/auth/login"],  # Final code: Please enable this one instead
            token_getter=self.get_token,
            is_revoked=self.is_revoked,
        ))

    async def is_revoked(self, request, payload):
        """
            Verify the collected access_token, checking whether it has been blacklisted/revoked
            (due to user logout function) or not
        """

        try:
            access_token = (request.headers['authorization']).replace("Bearer ", "")

            #  check if the access token has been blacklisted or not
            if is_token_revoked(MyRedis(asab.Config).get_rc(), access_token):
                return True
        except:
            pass
        return False

    async def get_token(self, request):
        """
           Collect and control access_token; Currently it simply forward the information
        """

        access_token = None
        try:
            access_token = (request.headers['authorization']).replace("Bearer ", "")
            access_token = access_token.encode()
        except:
            pass
        return access_token


if __name__ == '__main__':
    app = WebService()
    print("WorkLogs Service is running!")
    app.run()
