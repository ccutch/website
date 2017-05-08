

from notebooks.notebook import Notebook
from notebooks.entry import Entry
from notebooks.db_client import DatastoreClient

notebook_client = DatastoreClient()


__version__ = '1.0'
__author__ = 'Connor McCutcheon'

__all__ = ['Notebook', 'Entry', 'notebook_client']
