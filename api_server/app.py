from flask import Flask, Blueprint
from flask_restplus import Api

from api_server import notebook_routes
from frontend import view_routes


app = Flask(__name__)

api_routes = Blueprint(__name__, 'api_routes')
api = Api(api_routes, title='API for ccutch site', validate=True, doc='/api/')
notebook_routes.register(api)

app.register_blueprint(view_routes)
app.register_blueprint(api_routes)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
