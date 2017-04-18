
from flask import Blueprint
from flask_restplus import Api


api_routes = Blueprint(__name__, 'api_routes')
api = Api(api_routes, title='API for ccutch site', validate=True, doc='/api/')

from .notebook_routes import *  # noqa
# from .entry_routes import *     # noqa
# import .entry_routes  # noqa
