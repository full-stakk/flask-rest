"""This module handles calls to the database based on URIs it recieves."""
from flask.ext.restful import Resource, Api, fields, marshal, marshal_with, reqparse, abort
from flask import jsonify, Blueprint

import models

# Response definitions
user_fields = {
    'name': fields.String,
    'email': fields.String
}


class UserList(Resource):
    """Returns a list of users."""

    def get(self):
        """return a list of users."""
        users = [marshal(user, user_fields) for user in models.User.select()]

        return {'users': users}


class User(Resource):
    """Handles user methods."""

    def get(self):
        """get a user."""
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email is required', required=True)
        args = parser.parse_args()

        try:
            user = marshal(models.User.select().where(models.User.email == args['email']).get(), user_fields)
        except models.User.DoesNotExist:
            abort(404, message="User {} does not exist.".format(args['email']))
        else:
            return {'user': user}

    def put(self):
        """update a user."""
        return jsonify({'user': 'Unimplemented Method'})

    def delete(self):
        """delete a user."""
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help='email is required', required=True)
        args = parser.parse_args()

        query = models.User.delete().where(models.User.email == args['email'])
        query.execute()
        return('', 204)

    def post(self):
        """create a user."""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='name is required', required=True)
        parser.add_argument('email', type=str, help='email is required', required=True)
        parser.add_argument('password', type=str, help='password is requried', required=True)
        args = parser.parse_args()

        models.User.create(**args)
        return jsonify({'user':
                        {'message': 'Success'}
                        })
"""
Proxy to Blueprint module

arg 1 -- the location of the resource resources/users
arg 2 -- the namespace of the resources
"""
users_api = Blueprint('resources.users', __name__)
api = Api(users_api)

"""
Add resource logic to api routes

arg 1 -- resource to use
arg 2 -- the URI to use
arg 3 -- the name of the endpoint
"""

api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)

api.add_resource(
    User,
    '/user',
    endpoint='user'
)