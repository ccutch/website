
from google.cloud import datastore
from notebooks._helpers import Entity, _ensure_date
from gensim.summarization import summarize


class Entry(Entity):

    def __init__(self, notebook_id, title, body, abstract, created,
                 references=[], revised_id=None, key=None):
        self.notebook_key = db_client.key('Notebook', notebook_id)
        self.title = title
        self.body = body
        self.abstract = abstract or self.generate_abstract()
        self.references = references
        self.revised_id = revised_id
        self.created = _ensure_date(created)

    @property
    def notebook_id(self):
        return self.notebook_key.id

    def generate_abstract(self, overwrite=False):
        """ Generate an abstract for entry's body. This should be used when a
        user does not provide an abstract for their entry. If there is a user
        provided or previously generated abstract the function will raise an
        exception unlessage overwrite parameter is true. Guide for generating
        abstract based on this article about writing an effective abstract
        https://www.verywell.com/how-to-write-an-abstract-2794845."""
        if self.abstract != '' and not overwrite:
            raise Exception('Abstract generation attempted with existing'
                            ' abstract present.')

        self.abstract = summarize(word_count=250)
        return self.abstract

    def revise(self, new_data):
        from notebooks.db_client import DatastoreClient
        client = DatastoreClient()

        key = self.key
        new_entry = Entry(key=key, **new_data)
        self.key = None
        self.revised_id = new_entry.id

        return (client.SaveEntry(new_entry), client.SaveEntry(self))
