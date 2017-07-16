__author__ = 'zexxonn'

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db

import os.path

db.create_all()
print("Database created.")
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    pass
    #api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    #api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI,
                        SQLALCHEMY_MIGRATE_REPO,
                        api.version(SQLALCHEMY_MIGRATE_REPO))