
from notebooks import Notebook
from flask_restplus import Resource, Namespace, fields
from datetime import datetime
from api_server.app import api

ns = Namespace('Notebooks', title='Notebooks api')
api.add_namespace(ns, '/api/notebooks')


notebook_model = ns.model('Notebook', {
    'title': fields.String(required=True, description='Title of the notebook'),
    'description': fields.String(required=True),
    'created': fields.DateTime(readOnly=True, default=datetime.now)
})

notebook_list_model = ns.model('NotebookList', {
    'id': fields.Integer(readOnly=True,
                         description='Id of datastore key for notebook'),
    'notebook': fields.Nested(notebook_model)
})


@ns.route('/')
@ns.doc()
class NotebookListAPI(Resource):

    @ns.doc('list_notebooks')
    @ns.marshal_list_with(notebook_list_model)
    def get(self):
        notebooks = Notebook.get_list()
        # NOTE: Check if there is a nicer way to do this with flask restplus
        return map(lambda n: {'id': n.id, 'notebook': n}, notebooks)

    @ns.doc('create_notebooks')
    @ns.expect(notebook_model)
    @ns.marshal_with(notebook_model)
    def post(self):
        data = ns.marshal(api.payload, notebook_model)
        notebook = Notebook(**data)
        return notebook.save()


@ns.route('/<int:notebook_id>')
@ns.param('notebook_id')
@ns.doc()
class NotebookAPI(Resource):

    @ns.doc('get_notebook')
    @ns.marshal_with(notebook_model)
    def get(self, notebook_id):
        notebook = Notebook.get_by_id(notebook_id)
        return notebook

    @ns.doc('update_notebook')
    # @ns.expect(notebook_model)
    @ns.marshal_with(notebook_model)
    def put(self, notebook_id):
        data = ns.marshal(api.payload, notebook_model)
        data.pop('created')
        notebook = Notebook.get_by_id(notebook_id)
        notebook.update(data)
        return notebook.save()
