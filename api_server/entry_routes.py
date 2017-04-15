""" NOTE: This might be move to `notebook_routes.py` mapping
`/api/entries?notebook_id={notebook_id}` to
`/api/notebooks/{notebook_id}/entries` and so on.
"""

from notebooks import Entry
from flask_restplus import Resource, Namespace, fields
from datetime import datetime
from app import api


ns = Namespace('Entries', title='Entry api')
api.add_namespace(ns, '/api/entries')


entry_model = ns.model('Entry', {
    'title': fields.String(required=True, description='Title of the entry'),
    'notebook_id': fields.Integer(required=True),
    'abstract': fields.String(required=True),
    'body': fields.String(required=True),
    'references': fields.List(fields.String(), default=[]),
    'created': fields.DateTime(readOnly=True, default=datetime.now)
})

entry_list_model = ns.model('EntryList', {
    'id': fields.Integer(readOnly=True,
                         description='Id of datastore key for entry'),
    'entry': fields.Nested(entry_model)
})


@ns.route('/')
@ns.doc()
class EntryListAPI(Resource):

    list_parser = ns.parser()
    list_parser.add_argument('notebook_id', type=int, required=True)

    @ns.doc('list_entries', parser=list_parser)
    @ns.marshal_list_with(entry_list_model)
    def get(self):
        notebook_id = self.list_parser.parse_args()['notebook_id']

        entries = Entry.get_for_noteboook(notebook_id)
        # NOTE: Check if there is a nicer way to do this with flask restplus
        return map(lambda e: {'id': e.id, 'entry': e}, entries)

    @ns.doc('create_entry')
    @ns.expect(entry_model)
    @ns.marshal_with(entry_model)
    def post(self):
        data = ns.marshal(api.payload, entry_model)
        entry = Entry(**data)
        return entry.save()


@ns.route('/<int:entry_id>')
@ns.param('entry_id')
@ns.doc()
class EntryAPI(Resource):

    @ns.doc('get_entry')
    @ns.marshal_with(entry_model)
    def get(self, entry_id):
        entry = Entry.get_by_id(entry_id)
        return entry

    # @ns.doc('update_notebook')
    # # @ns.expect(notebook_model)
    # @ns.marshal_with(notebook_model)
    # def put(self, notebook_id):
    #     data = ns.marshal(api.payload, notebook_model)
    #     data.pop('created')
    #     notebook = Notebook.get_by_id(notebook_id)
    #     notebook.update(data)
    #     return notebook.save()
