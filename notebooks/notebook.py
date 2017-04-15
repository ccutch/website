
from google.cloud import datastore
from datetime import datetime
from dateutil.parser import parse
from notebooks.db_helper import db_client
from notebooks.entry import Entry


class Notebook(object):
    """
    """

    def __init__(self, title, description, created=None, key=None):
        self.key = key
        self.title = title
        self.description = description

        if type(created) == datetime:
            self.created = created
        elif type(created) == str:
            self.created = parse(created)
        else:
            self.created = None

    @staticmethod
    def get_list():
        query = db_client.query(kind='Notebook')
        return map(lambda n: Notebook(key=n.key, **n), query.fetch())

    @staticmethod
    def get_by_id(id):
        key = db_client.key('Notebook', id)
        return Notebook(
            key=key,
            **db_client.get(key)
        )

    @property
    def id(self):
        """ Short cut to getting key property id """
        if not self.key:
            return None

        return self.key.id

    def add_entry(self, entry_data):
        entry = Entry(**entry_data)
        return entry.save()

    def get_entries(self):
        return Entry.get_for_noteboook(self.id)

    def update(self, updates):
        """ Update fields of notebook.

        This is used to do many updates on the
        notebook instance rather than going field by field.

        :type updates: dict
        :param updates: updates to be applied

        :rtype: :class:`notebooks.Notebook`
        :returns: updated notebook
        """
        for name, value in updates.items():
            setattr(self, name, value)

        return self

    def save(self):
        """ Save notebook to database.

        :rtype: :class:`notebooks.Notebook`
        :returns: notebook instance
        """
        if not self.key:
            self.key = db_client.key('Notebook')

        entity = datastore.Entity(key=self.key)
        entity.update({
            'title': self.title,
            'created': self.created,
            'description': self.description
        })

        db_client.put(entity)
        return self
