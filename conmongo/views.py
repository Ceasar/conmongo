from bson.objectid import ObjectId
from flask import request, g, abort
from flask.views import MethodView

from json import jsonify


class BSONAPI(MethodView):
    """
    Convenience wrapper on MethodView for BSON entities.

    Provides default implementations of HTTP methods.

    To use, override `collection_name` appropriately.
    """
    @property
    def collection_name(self):
        raise NotImplementedError()

    @property
    def collection(self):
        return getattr(g.db, self.collection_name)

    def validate(self, entity):
        """Determine if an entity is valid for insertion into the database."""
        return True

    def post(self):
        """
        Create a new entity.
        """
        entity = request.form.to_dict()
        try:
            self.validate(entity)
        except AssertionError:
            abort(400)
        else:
            self.collection.insert(entity)
            return entity

    def get(self, _id=None):
        """
        Show data about an entity.

        If `_id` is `None`, show data about the collection.
        """
        if _id is None:
            limit = int(request.args.get('limit', 10))
            offset = int(request.args.get('offset', 0))
            entities = list(self.collection.find(skip=offset, limit=limit))
            return {'results': entities}
        else:
            entity = self.collection.find_one({"_id": ObjectId(_id)})
            return entity

    def patch(self):
        pass

    def delete(self):
        pass

    def dispatch_request(self, *args, **kwargs):
        rv = super(BSONAPI, self).dispatch_request(*args, **kwargs)
        return jsonify(rv)
