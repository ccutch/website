from os import path
from flask import Flask, Blueprint, send_from_directory
from flask_restplus import Api
from server import notebook_routes, frontend_routes

root_dir = path.abspath(path.dirname(path.dirname(__file__)))
frontend_dir = path.join(root_dir, 'frontend')


api_routes = Blueprint(__name__, 'api_routes')
api = Api(api_routes, title='API for ccutch site', validate=True, doc='/api/')
notebook_routes.register(api)

app = Flask(__name__)

app.register_blueprint(api_routes)
app.register_blueprint(frontend_routes.routes)


@app.errorhandler(404)
def handle_error(error):
    return send_from_directory(frontend_dir, 'index.html')


if __name__ == '__main__':
    app.run(port=8080, debug=True)
