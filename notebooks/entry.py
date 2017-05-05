
from google.cloud import datastore
from datetime import datetime
from dateutil.parser import parse
from notebooks.db_helper import DatabaseEntity


class Entry(DatabaseEntity):

    def __init__(self, notebook_id, title, abstract, body, created,
                 references=[], revised_id=None, key=None):
        super(Entry, self).__init__(key=key)
        self.notebook_key = db_client.key('Notebook', notebook_id)
        self.title = title
        self.abstract = abstract
        self.body = body
        self.references = references
        self.revised_id = revised_id

        if type(created) == str:
            self.created = parse(created)
        else:
            self.created = created

    def revise(self, new_data):
        key = self.key
        new_entry = Entry(key=key, **new_data)
        self.key = db_client.key('Entry', parent=self.notebook_key)
        self.revised_id = new_entry.id

        return new_entry.save(), self.save()
