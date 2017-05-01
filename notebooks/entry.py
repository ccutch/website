
from google.cloud import datastore
from datetime import datetime
from dateutil.parser import parse
from notebooks.db_helper import DatabaseEntity


class Entry(DatabaseEntity):

    excluded_fields = ['abstract', 'body']
    fields = [
        'title', 'abstract', 'created',
        'body', 'references', 'revised_id'
    ]

    def __init__(self, notebook_id, title, abstract, body, created,
                 references=[], revised_id=None, key=None):
        super(Entry, self).__init__(key=key)
        self.parent_key = db_client.key('Notebook', notebook_id)
        self.title = title
        self.abstract = abstract
        self.body = body
        self.references = references
        self.revised_id = revised_id

        if type(created) == datetime:
            self.created = created
        elif type(created) == str:
            self.created = parse(created)
        else:
            self.created = None

    @staticmethod
    def get_for_noteboook(notebook_id):
        query = db_client.query(kind='Entry')
        query.ancestor = db_client.key('Notebook', notebook_id)
        return map(lambda e: Entry(
            key=e.key,
            notebook_id=e.key.parent.id,
            **e), query.fetch())

    @staticmethod
    def get_by_id(entry_id, notebook_id):
        key = db_client.key('Notebook', notebook_id, 'Entry', entry_id)
        e = db_client.get(key)
        if not e:
            return None
        e['notebook_id'] = notebook_id
        return Entry(key=key, **e)

    @property
    def id(self):
        """ Short cut to getting key property id """
        if not self.key:
            return None

        return self.key.id

    @property
    def notebook_id(self):
        """ Short cut to getting key property id of parent notebook """
        return self.notebook_key.id

    def revise(self, new_data):
        key = self.key
        new_entry = Entry(key=key, **new_data)
        self.key = db_client.key('Entry', parent=self.notebook_key)
        self.revised_id = new_entry.id

        return new_entry.save(), self.save()
