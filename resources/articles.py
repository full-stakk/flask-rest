"""This module handles calls to the database based on URIs it recieves."""
from flask.ext.restful import (Resource, Api, fields, marshal_with, marshal,
                               reqparse, abort)
from flask import jsonify, Blueprint, make_response, g
from auth import auth

import json
import models
import datetime

# Response definitions
article_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'body': fields.String,
    'created_at': fields.DateTime
}


def article_or_404(id):
    try:
        article = models.Article.select().where(models.Article.id == id).get()
    except models.Article.DoesNotExist:
        abort(404, message="Article does not exist.")
    else:
        return article


class ArticleList(Resource):
    """Returns a list of articles."""
    def get(self):
        """return a list of articles."""
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help="Email is required", required=True)
        args = parser.parse_args()

        if(args['email'] == 'all'):
            articles = [marshal(article, article_fields) for article in models.Article.select()]
        else:
            user = models.User.select().where(models.User.email == args['email']).get()
            articles = [marshal(article, article_fields) for article in models.Article.select().where(models.Article.user == user)]

        return articles

    @auth.login_required
    @marshal_with(article_fields)
    def post(self):
        """create a articles."""
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, help="Email is required", required=True)
        parser.add_argument('title', type=str, help="Title is required", required=True)
        parser.add_argument('body', type=str, help="Article is required", required=True)
        args = parser.parse_args()

        article = models.Article.create(
            title=args['title'],
            body=args['body'],
            user=g.user,
            created_at=datetime.datetime.now()
        )
        return (article, 201, {
            'id': article.id
        })


class Article(Resource):
    """Handles article methods."""

    @marshal_with(article_fields)
    def get(self):
        """get a article."""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, help="Id is required", required=True)
        args = parser.parse_args()
        return article_or_404(args['id'])

    @auth.login_required
    def put(self, id):
        """update a article."""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, help="Id is required", required=True)
        args = parser.parse_args()

        try:
            article = models.Article.select().where(
                models.Article.user == g.user,
                models.Article.id == id
            ).get()
        except models.Article.DoesNotExist:
            return make_response(json.dumps(
                {'error': 'That article does not exist'}
            ), 403)

        query = article.update(**args)
        query.execute()
        return (
                models.Article.select().where(models.Article.id == args['id']),
                200,
                {'id': id}
                )

    @auth.login_required
    def delete(self, id):
        """delete a articles."""
        try:
            article = models.Article.select().where(
                models.Article.user == g.user,
                models.Article.id == id
            ).get()
        except models.Article.DoesNotExist:
            return make_response(json.dumps(
                {'error': 'That article does not exist'}
            ), 403)

        query = article.delete()
        query.execute()
        return article.id, 204, {'message': 'Deleted'}

"""
Proxy to Blueprint module

arg 1 -- the location of the resource resources/users
arg 2 -- the namespace of the resources
"""
articles_api = Blueprint('resources.articles', __name__)
api = Api(articles_api)

"""
Add resource logic to api routes

arg 1 -- resource to use
arg 2 -- the URI to use
arg 3 -- the name of the endpoint
"""

api.add_resource(
    ArticleList,
    '/articles',
    endpoint='articles'
)

api.add_resource(
    Article,
    '/article',
    endpoint='article'
)
