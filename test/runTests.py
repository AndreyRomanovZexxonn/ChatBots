__author__ = 'zexxonn'

import unittest
from TestFxRate import TestForexPython
from TestOpenWeatherMap import TestOpenWeatherMap

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestForexPython)
    unittest.TextTestRunner(verbosity=3).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestOpenWeatherMap)
    unittest.TextTestRunner(verbosity=3).run(suite)
