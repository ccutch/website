
from google.cloud import datastore
from notebooks._helpers import Entity, _ensure_date


class Entry(Entity):

    def __init__(self, notebook_id, title, abstract, body, created,
                 references=[], revised_id=None, key=None):
        self.notebook_key = db_client.key('Notebook', notebook_id)
        self.title = title
        self.abstract = abstract
        self.body = body
        self.references = references
        self.revised_id = revised_id
        self.created = _ensure_date(created)

    @property
    def notebook_id(self):
        return self.notebook_key.id

    def revise(self, new_data):
        key = self.key
        new_entry = Entry(key=key, **new_data)
        self.key = db_client.key('Entry', parent=self.notebook_key)
        self.revised_id = new_entry.id

        return new_entry.save(), self.save()
