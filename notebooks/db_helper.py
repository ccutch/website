
from google.cloud import datastore


PROJECT_ID = 'ccutch-blog'

db_client = datastore.Client(project=PROJECT_ID)
