"""

This modules implements the database wrapper for the central WSGI application
object.

"""

from flask import g
from pymongo import MongoClient

from json import JSONEncoder


PK = '_id'
PK_TYPE = 'string'


def MongoApp(app):
    @app.before_request
    def before_request():
        g._connection = connection = MongoClient()
        g.db = getattr(connection, app.config['DATABASE'])

    @app.teardown_request
    def teardown_request(exception):
        g._connection.close()

    def add_resource(rule, method_view):
        """
        Create API endpoints for /entities/ and /entities/<id>.

        :param rule: the URL rule a string
        :param endpoint: the endpoint for the registered URL rule.
        :param method_view: the MethodView to call when serving a request to
                            the provided endpoint
        """

        # Convert the class into an actual view function that can be used
        # with the routing system
        view_func = method_view.as_view(rule)

        # route for "/entities/"
        app.add_url_rule(rule,
                         view_func=view_func,
                         methods=['GET', 'POST'])

        # TODO: Might PATCH make more sense than PUT?
        # route for "/entities/<id>"
        app.add_url_rule('%s<%s:%s>' % (rule, PK_TYPE, PK),
                         view_func=view_func,
                         methods=['GET', 'PUT', 'DELETE'])
    app.add_resource = add_resource

    def resource(rule):
        """
        A decorator that is used to register a MethodView for a resource.

            @app.resource('/users/')
            class UserAPI(view.BSONAPI):
                pass

        Is equivalent to the folowing::

            class UserAPI(view.BSONAPI):
                pass
            app.add_resource('/users/', UserAPI)
        """
        def decorator(method_view):
            add_resource(rule, method_view)
            return method_view

        return decorator
    app.resource = resource

    return app
