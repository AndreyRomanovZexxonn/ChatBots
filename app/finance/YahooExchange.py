__author__ = 'zexxonn'

import re
from yahoo_finance import Currency, Share

def prepareCurrencyName(ccyName):
    regex = re.compile(" |/")
    return regex.sub("", ccyName).replace("\\", "")

def getExchangeRate(ccyName):
    ccy = Currency(ccyName)
    return ccy.get_rate()

