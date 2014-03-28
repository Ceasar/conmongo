import flask
from pytest import fixture

from conmongo.json import dumps, jsonify
from conmongo.views import BSONAPI


@fixture
def app():
    app = flask.Flask(__name__)
    return app


class Resource(BSONAPI):
    collection_name = 'resource'


@fixture
def resource():
    return Resource()


def test_dumps():
    obj = range(10)
    assert dumps(obj) == str(obj)
    obj = {'a': 1, 'b': 2}
    assert dumps(obj) == str(obj).replace("'", '"')


def test_jsonify(app):
    with app.test_request_context("/"):
        obj = {'a': 1}
        response = jsonify(obj)
        assert response.data == '{\n  "a": 1\n}'
        assert response.status_code == 200
        assert response.mimetype == 'application/json'


def test_resource(resource):
    assert resource.collection_name == 'resource'
