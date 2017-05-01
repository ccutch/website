
from google.cloud import datastore
from datetime import datetime
from dateutil.parser import parse
from notebooks.db_helper import DatabaseEntity
from notebooks.entry import Entry


class Notebook(DatabaseEntity):
    """
    """
    excluded_fields = ['description']
    fields = [
        'title',
        'created',
        'description'
    ]

    def __init__(self, title, description, created=None, key=None):
        super(Notebook, self).__init__(key=key)
        self.title = title
        self.description = description

        if type(created) == datetime:
            self.created = created
        elif type(created) == str:
            self.created = parse(created)
        else:
            self.created = None

    @property
    def entries(self):
        return Entry.get_for_noteboook(self.id)

    def add_entry(self, entry_data):
        entry = Entry(**entry_data)
        return entry.save()
