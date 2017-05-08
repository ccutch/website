from __future__ import print_function

import os

from google.cloud import datastore
from notebooks.entry import Entry
from notebooks.notebook import Notebook


PROJECT_ID = os.getenv('project', 'ccutch-blog')


class DatastoreClient(object):

    NOTEBOOK_KIND = 'Notebook'
    ENTRY_KIND = 'Entry'

    def __init__(self):
        self.client = datastore.Client(project=PROJECT_ID)

    def _put_entity(self, key, fields, excluded=()):
        """ Creates entity and saves to datastore under given key with the given
        fields. All fields are queriable unless in excluded list.
        """

        entity = datastore.Entity(
            key=key,
            exclude_from_indexes=excluded
        )
        entity.update(fields)
        self.client.put(entity)

    def ListNotebooks(self):
        query = self.client.query(kind=self.NOTEBOOK_KIND)
        return map(lambda n: Notebook(key=n.key, **n), query.fetch())

    def GetNotebook(self, notebook_id):
        key = self.client.key(self.NOTEBOOK_KIND, notebook_id)
        notebook_data = self.client.get(key)
        return Notebook(key=key, **notebook_data)

    def SaveNotebook(self, notebook):
        if not notebook.key:
            notebook.key = self.client.key(self.NOTEBOOK_KIND)

        self._put_entity(notebook.key, {
            'title': notebook.title,
            'created': notebook.created,
            'description': notebook.description,
        }, excluded=['description'])
        return notebook

    def ListEntries(self, notebook_id):
        query = self.client.query(
            kind=self.ENTRY_KIND, ancestor=self.NOTEBOOK_KIND)
        return map(
            lambda e: Entry(key=e.key, notebookd_id=e.key.parent.id, **e),
            query.fetch())

    def GetEntry(self, notebook_id, entry_id):
        key = self.client.key(
            self.NOTEBOOK_KIND, notebook_id,
            self.ENTRY_KIND, entry_id)
        entry_data = self.client.get(key)
        return Entry(key=key, notebook_id=notebook_id, **entry_data)

    def SaveEntry(self, entry):
        if not entry.key:
            entry.key = self.client.key(
                self.ENTRY_KIND, parent=entry.notebook_key)

        self._put_entity(entry.key, {
            'notebook_id': entry.notebook_id,
            'title': entry.title,
            'abstract': entry.abstract,
            'body': entry.body,
            'created': entry.created,
            'references': entry.references,
            'revised_id': entry.revised_id
        }, excluded=['title', 'abstract', 'body', 'references'])
        return entry

