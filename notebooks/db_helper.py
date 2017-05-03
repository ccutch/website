
from google.cloud import datastore


PROJECT_ID = 'ccutch-blog'


class DatabaseEntity(object):

    fields = None
    excluded_fields = []
    client = datastore.Client(project=PROJECT_ID)

    def __init__(self, key):
        self.key = key
        self.parent_key = None

    @property
    def id(self):
        """ Short cut to getting key property id """
        if not self.key:
            return None

        return self.key.id

    @classmethod
    def get_by_id(cls, id, **kwargs):
        fields = [cls.__name__, id]
        for k, v in kwargs.iteritems():
            fields.append(k, v)
        return cls(key=key, **cls.client.get(key))

    @classmethod
    def get_list(cls):
        query = cls.client.query(kind=cls.__name__)
        return map(lambda e: cls(key=e.key, **e), query.fetch())

    def save(self):
        """ Save entity to datastore

        :rtype: :class:`notebooks.db_helper.DatabaseEntity`
        :returns: entity instance
        """
        if self.fields is None:
            raise Exception("Database fields not defined")

        if self.key is None:
            self.key = self.client.key(
                self.__class__.__name__, parent=self.parent_key)

        entity = datastore.Entity(
            key=self.key, exclude_from_indexes=self.excluded_fields)
        entity.update({
            f: getattr(self, f) for f in self.fields
        })

        self.client.put(entity)
        return self

    def update(self, updates):
        """ Update fields of Entity.

        This is used to do many updates on the
        notebook instance rather than going field by field.

        :type updates: dict
        :param updates: updates to be applied

        :rtype: :class:`notebooks.db_helper.DatabaseEntity`
        :returns: updated instance
        """
        for name, value in updates.items():
            setattr(self, name, value)

        return self.save()
