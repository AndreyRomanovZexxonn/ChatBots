__author__ = 'zexxonn'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

webapp = Flask(__name__)
webapp.config.from_object('config')
db = SQLAlchemy(webapp)

from app import server, models
