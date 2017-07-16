__author__ = 'zexxonn'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False' \
        if os.environ.get('DATABASE_URL') is None else os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

OPEN_WEATHER_MAP_API_KEY = "7fa8263646f1ba04927e72442918d7c2"
FB_VERIFY_TOKEN = "zexxonn1988"
FB_PAGE_ACCESS_TOKEN = "EAAJdDYjAPMEBAJK9ZAM8STqEGwCPSVdPPWNnG0nKSLAULSeN2pcOVWs4ARLZB50efibT9FtBbOeL5UcZAAU8ZABIBiXfBSQZACSFiZCNCS7DnSRIsYDnIB08uv9hsMqHceIsq1JKqB2VXoQuBmLqz3w0ZBZC9ZBn0SfFuIlD1Cug1FZCJBZCtc5ZCmen"