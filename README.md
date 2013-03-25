# conmongo

Simple mongodb integration for Flask.

# Rationale

Make it easy to create an API for a mongodb.

# Quickstart

## A Minimal Application

```python
from flask import Flask
from conmongo import MongoApp
from conmongo.views import BSONAPI

app = MongoApp(Flask(__name__))
app.config['DATABASE'] = 'test'

@app.resource('/users/')
class UserAPI(BSONAPI):
    collection_name = 'users'

if __name__ == '__main__':
    app.run()
```

Now, in another terminal, start a `mongod` instance.

Run the above as a flask app and then head over to `http://localhost:5000/users/`.

You probably won't see much as we've yet to add anything to the database.

```json
{
    results: [ ]
}
```

Let's add a record now.

```bash
curl -v --data "name=john&email=john@example.com" http://127.0.0.1:5001/users/
```

Now refresh!

```json
{
    results: [
        {
            _id: "514fb3fd8d3fa362cff26f61",
            name: "john",
            email: "john@example.com"
        }
    ]
}
```

Your `_id` value may by different. If you copy it and append it to the URL you can inspect `john` in detail.

```json
{
    _id: "514fb3fd8d3fa362cff26f61",
    name: "john",
    email: "john@example.com"
}
```

## Validation

At the moment, the server does no validation and create documents in our database for any incoming valid POST request, regardless of whether or not it has a reasonable schema.

We can change that by adding a `validate` method to our `UserAPI` model like so:

```python
@app.resource('/users/')
class UserAPI(BSONAPI):
    collection_name = 'users'

    def validate(self, entity):
        assert 'name' in entity
```

`validate` is automatically called on the data that comes from any incoming POST request. If `validate` fails, a 400 (bad request) error is thrown.
