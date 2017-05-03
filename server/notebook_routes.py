
from flask import Blueprint, request, jsonify
from marshmallow import fields, Schema
from notebooks.notebook import Notebook


# routes = Blueprint('notebook_api', __name__)
routes = Blueprint(__name__, 'notebook_api')


class NotebookSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    created = fields.DateTime(required=True)


class NotebookList(Schema):
    id = fields.Integer()
    notebook = fields.Nested(NotebookSchema)


def _json_response(schema, data):
    res = schema.dump(data)
    return jsonify(res.data)


@routes.route('/', methods=['GET'])
def list_notebooks():
    """ Gets a list of notebooks
    ---
    get:
        description: Gets list of notebooks
        responses:
            200:
                description: List of notebooks is returned
                schema:
                    $ref: '#/definitions/NotebookList'
    """
    notebooks = Notebook.get_list()
    return _json_response(
        NotebookList(many=True),
        [{'id': n.id, 'notebook': n} for n in notebooks])


@routes.route('/', methods=['POST'])
def create_notebook():
    """ Creates a notebook
    ---
    post:
        description: Creates a notebook
        consumes:
        - application/json
        parameters:
        - name: notebook_data
          in: body
          schema:
            $ref: '#/definitions/Notebook'
        responses:
            200:
                description: Newly created notebook
                schema:
                    $ref: '#/definitions/Notebook'
    """
    data, errors = notebook_schema.load(request.get_json())
    if errors:
        return jsonify(errors), 400
    notebook = Notebook(**data)
    notebook.save()
    return _json_response(NotebookSchema(), notebook)


@routes.route('/<int:notebook_id>', methods=['GET', 'PUT'])
def get_update_notebook(notebook_id):
    """ Get and, if updates are given, update notebook
    ---
    get:
        description: Get notebook by id
        parameters:
        - in: path
          name: notebook_id
          type: string
        responses:
            200:
                description: Notebook from database
                schema:
                    $ref: '#/definitions/Notebook'
            404:
                description: Error message

    put:
        description: update notebook
        consumes:
        - application/json
        parameters:
        - in: path
          name: notebook_id
          type: string
        - name: notebook_data
          in: body
          schema:
            $ref: '#/definitions/Notebook'
        responses:
            200:
                description: Newly created notebook
                schema:
                    $ref: '#/definitions/Notebook'
    """
    notebook = Notebook.get_by_id(notebook_id)
    if request.method == 'PUT':
        pass
    return _json_response(NotebookSchema(), notebook)
