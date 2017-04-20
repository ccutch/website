
from flask import Blueprint


routes = Blueprint(
    # __name__,
    'angular',
    'angular_frontend',
    static_folder='frontend',
    static_url_path='')