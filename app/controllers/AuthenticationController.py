from flask_bcrypt import Bcrypt
import datetime
from flask import jsonify
from flask_api import status
from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, get_raw_jwt, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity)

from app.models.revoked_token import RevokedTokens
from app.models.user import Users

flask_bcrypt = Bcrypt()


class Hello(Resource):
    def get(self):
        response = jsonify({'nice': 'Your journey has just begun little one'})
        response.status_code = status.HTTP_200_OK
        return response


# This class handles the user registration
class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='Please provide us with a username', required=True)
        parser.add_argument('password', help='Please provide us with a password', required=True)
        parser.add_argument('phone_number', help='Please provide us with your phone number', required=True)
        parser.add_argument('role_id', help='Please provide us with the user role', required=True)
        parser.add_argument('email')
        data = parser.parse_args()
        # with db.transaction():

        try:

            users = Users()
            users.username = data['username']
            users.email = data['email']
            users.role_id = data['role_id']
            users.password = flask_bcrypt.generate_password_hash(data['password']).decode('utf-8')
            users.phone_number = data['phone_number']
            users.save()

            expires = datetime.timedelta(days=60)
            access_token = create_access_token(identity=data['phone_number'], expires_delta=expires)
            refresh_token = create_refresh_token(identity=data['phone_number'])
            response = jsonify({'status': 'Success', 'message': 'A new user has been created successfully',
                                'access_token': access_token, 'refresh_token': refresh_token})
            response.status_code = status.HTTP_201_CREATED
            return response
        except Exception as e:

            if 'Duplicate' in str(e):
                response = jsonify({'status': 'Fail', 'message': 'The user with the provided details already exists'})
                response.status_code = status.HTTP_409_CONFLICT
                return response
            else:
                response = jsonify(
                    {'status': 'Fail',
                     'message': 'There was an issue in trying to save the user. Please contact support at '
                                'support@info.com',
                     })
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return response


# Logic which takes care of on how a user will login to the system
class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help='Please provide us with your email address', required=True)
        parser.add_argument('password', help='Please provide us with a password', required=True)
        data = parser.parse_args()
        # Fetch the user details
        try:
            current_user = Users.join('roles', 'roles.id', '=', 'users.role_id') \
                .where('email', data['email']).select('users.*', 'roles.role_code').first()
            if current_user is None:
                response = jsonify({'status': 'Fail', 'message': 'The user does not exist in the system'})
                response.status_code = status.HTTP_200_OK
                return response

            if flask_bcrypt.check_password_hash(current_user.password, data['password']):
                expires = datetime.timedelta(days=60)
                access_token = create_access_token(identity=data['email'], expires_delta=expires)
                refresh_token = create_refresh_token(identity=data['email'])
                response = jsonify(
                    {'status': 'Success', 'message': 'Logged in successfully', 'access_token': access_token,
                     'refresh_token': refresh_token,
                     'data': current_user.serialize()})
                response.status_code = status.HTTP_202_ACCEPTED
                return response
            else:
                response = jsonify({'status': 'Fail', 'message': 'You have entered wrong credentials combination'})
                response.status_code = status.HTTP_401_UNAUTHORIZED
                return response
        except Exception as err:
            response = jsonify(
                {'status': 'Fail', 'message': 'There was an issue with the request please contact support'
                                              ' if the issue persists.'})
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return response


# Used to logout the user from the system and also revoke their jwt token saved
class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokens()
            revoked_token.jti = jti
            revoked_token.save()
            response = jsonify({'status': 'Success', 'message': 'You have successfully logged out'})
            response.status_code = status.HTTP_200_OK
            return response
        except Exception as err:
            response = jsonify(
                {'status': 'Fail', 'message': 'There was an issue with the request please contact support'
                                              ' if the issue persists.'})
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return response


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        response = jsonify({
            'status': 'Success',
            'message': 'Access token refreshed successfully',
            'access_token': access_token
        })
        response.status_code = status.HTTP_200_OK
        return response
