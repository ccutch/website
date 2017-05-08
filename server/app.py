import sys
import json
import yaml
from os import path
from flask import Flask, Blueprint, send_from_directory, jsonify
from server import notebook_routes, frontend_routes
from swagger import spec, load_spec


root_dir = path.abspath(path.dirname(path.dirname(__file__)))
frontend_dir = path.join(root_dir, 'frontend')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.register_blueprint(notebook_routes.routes, url_prefix='/api/notebooks')
app.register_blueprint(frontend_routes.routes)


@app.errorhandler(404)
def handle_error(error):
    return send_from_directory(frontend_dir, 'index.html')


@app.route('/swagger.json')
def serve_swagger():
    load_spec()
    return jsonify(spec.to_dict())


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'generate_openapi':
        ctx = app.test_request_context()
        ctx.push()
        load_spec()
        spec_dict = spec.to_dict()
        with open('openapi.yaml', 'w') as file:
            yaml.safe_dump(
                json.loads(json.dumps(spec_dict)),
                file,
                allow_unicode=True,
                default_flow_style=False)
    else:
        app.run(port=8080, debug=True)
