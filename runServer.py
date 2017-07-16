__author__ = 'zexxonn'

from app import webapp
from setupTools import setupDatabase

setupDatabase()
webapp.run(debug=True)