from __future__ import absolute_import

from datetime import datetime

from bson.objectid import ObjectId
from flask import json, current_app, request
from werkzeug.http import http_date


class JSONEncoder(json.JSONEncoder):
    """
    Custom encoder for BSON objects.

    (ObjectID can't be serialized so we have our own encoder.)
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return http_date(obj)
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


# The following should be come redundant once Flask 0.10 is released


def dumps(obj, **kwargs):
    """Serialize ``obj`` to a JSON formatted ``str`` by using the application's
    configured encoder (:attr:`~flask.Flask.json_encoder`) if there is an
    application on the stack.

    This function can return ``unicode`` strings or ascii-only bytestrings by
    default which coerce into unicode strings automatically.  That behavior by
    default is controlled by the ``JSON_AS_ASCII`` configuration variable
    and can be overriden by the simplejson ``ensure_ascii`` parameter.
    """
    return json.dumps(obj, cls=JSONEncoder, **kwargs)


def jsonify(*args, **kwargs):
    return current_app.response_class(dumps(dict(*args, **kwargs),
        indent=None if request.is_xhr else 2),
        mimetype='application/json')
