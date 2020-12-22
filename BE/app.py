from flask      import Flask
from flask_cors import CORS
from flask.json import JSONEncoder
from decimal    import Decimal
from datetime   import datetime

from view    import ProductView, OrderView, AccountView, SellerView


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return JSONEncoder.default(self, obj)

def create_app(test_config=None):
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    CORS(app, resources={r'*': {'origins': '*'}})

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)
    return app
