
from google.cloud import datastore
from notebooks.entry import Entry
from notebooks._helpers import Entity, _ensure_date


class Notebook(Entity):
    """ Notebook object

    :type title: str
    :param title: Title of notebook

    :type description: str
    :param description: description of notebook

    :type created: datetime
    :param created: timestamp when notebook was created

    :type key: class`google.cloud.datastore.Key`
    :param key: datastore key object. Created on save if None
    """

    def __init__(self, title, description, created, key=None):
        self.key = key
        self.title = title
        self.description = description
        self.created = _ensure_date(created)

    @property
    def entries(self):
        return Entry.get_for_noteboook(self.id)

    def add_entry(self, entry_data):
        entry = Entry(**entry_data)
        return entry.save()
