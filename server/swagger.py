
from __future__ import print_function
from flask import current_app
from pprint import pprint
from apispec import APISpec, Path, utils
from apispec.ext.flask import flaskpath2swagger
from notebook_routes import NotebookSchema, NotebookList, routes


spec = APISpec(
    title='Swagger spec for google endpoints',
    version='1.0.1',
    plugins=[
        'apispec.ext.flask',
        'apispec.ext.marshmallow'
    ]
)


def load_spec():
    spec.definition('Notebook', schema=NotebookSchema)
    spec.definition('NotebookList', schema=NotebookList)
    # spec.add_path(view=notebook_routes.list_notebooks)
    add_paths_for_blueprint(spec, routes, exclude=('serve_swagger',))


# Blueprint helpers below
def path_from_rule(spec, rule, **kwargs):
    """Path helper that allows passing a Flask url Rule object."""
    path = flaskpath2swagger(rule.rule)
    view = current_app.view_functions.get(rule.endpoint)
    # Get operations from view function docstring
    operations = utils.load_operations_from_docstring(view.__doc__)
    return Path(path=path, operations=operations)

spec.register_path_helper(path_from_rule)


def add_paths_for_blueprint(spec, blueprint, exclude=()):
    bp_name = blueprint.name
    for r in current_app.url_map._rules:
        pprint(r.endpoint)
        endpoint = r.endpoint.split('.')

    for r in current_app.url_map.iter_rules():
        ep = r.endpoint.split('.')
        if len(ep) == 1:  # App endpoint, not processed here
            continue
        elif len(ep) >= 2:  # Blueprint endpoint
            i = len(ep) - 1
            endpoint = ep[i]
            bp = '.'.join(ep[:i])
            print(bp)
            if bp == bp_name and endpoint not in exclude:
                spec.add_path(rule=r)
        else:
            raise ValueError("Not valid endpoint?", r.endpoint)
