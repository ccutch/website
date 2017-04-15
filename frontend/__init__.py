
import os
from flask import Blueprint

view_routes = Blueprint(__name__, 'views', static_folder='./frontend')


@view_routes.route('/static/<path:path>')
def send_script(path):
    return view_routes.send_static_file(path)


@view_routes.route('/')
@view_routes.route('/<path:path>')
def send_index(path=None):
    return view_routes.send_static_file('index.html')
