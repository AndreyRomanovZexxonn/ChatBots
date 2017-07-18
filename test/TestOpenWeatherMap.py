__author__ = 'zexxonn'

import unittest
from app.server import getInfoFromOpenWeatherMap

class TestOpenWeatherMap(unittest.TestCase):

    def testWeather(self):
        res = getInfoFromOpenWeatherMap(55.751244, 37.618423)
        self.assertRegexpMatches(res, "Description: Moscow.*")
