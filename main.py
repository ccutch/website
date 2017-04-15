
from flask import Flask
from api_server import api_routes
from frontend import view_routes

app = Flask(__name__)
app.register_blueprint(view_routes)
app.register_blueprint(api_routes)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
