from flask import Blueprint
from flask_restful import Api

from app.controllers import AuthenticationController

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Auth routes
api.add_resource(AuthenticationController.Hello, '/')
api.add_resource(AuthenticationController.UserRegistration, '/signup')
api.add_resource(AuthenticationController.UserLogin, '/login')
api.add_resource(AuthenticationController.UserLogout, '/logout')
api.add_resource(AuthenticationController.TokenRefresh, '/refreshToken')