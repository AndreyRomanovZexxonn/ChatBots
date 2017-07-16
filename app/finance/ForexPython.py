__author__ = 'zexxonn'

from forex_python.converter import CurrencyRates
from YahooExchange import prepareCurrencyName
from datetime import datetime

timeFormat = "%Y.%m.%d"
timeFormatForUser = "yyyy.mm.dd"
currencyFormat = "XXXYYY"

def dateToStr(d):
    return d.strftime(timeFormat)

def getExchangeRate(ccyPairInfo):

    values = ccyPairInfo.strip().split(" ")
    if not values:
        return "Can\'t provide Fx Rate.\nYou didn\'t provide enough information."

    if len(values) >= 3:
        return "Can\'t provide Fx Rate.\nYou provide incorrect information."

    ccyPairStr    = None
    if len(values) >= 1:
        ccyPairStr = values[0].strip()
    preparedCcyPair = prepareCurrencyName(ccyPairStr).upper()

    fxRateDateStr = None
    if len(values) == 2:
        fxRateDateStr = values[1].strip()

    fxRateDate = None
    try:
        fxRateDate = datetime.strptime(fxRateDateStr, '%Y.%m.%d') \
                            if fxRateDateStr else datetime.now()
    except Exception as ex:
        return "Can\'t provide Fx Rate.\n" \
               "Date provided in incorrect format.\n" \
               "Format has to be {}".format(timeFormatForUser)



    if len(preparedCcyPair) != 6:
        return "Can\'t provide Fx Rate.\n" \
               "You asked Fx Rate for incorrect Currency Pair {}.\n" \
               "Currency Pair has to be in format \"{}\"".format(preparedCcyPair, currencyFormat)


    if fxRateDate > datetime.now():
        return "Can\'t provide Fx Rate.\n" \
               "You asked Fx Rate for date in the future.\n" \
               "{} > (today) = {}".format(dateToStr(fxRateDate), dateToStr(datetime.now()))

    accCcy, undCcy = preparedCcyPair[:3], preparedCcyPair[3:]
    cr = CurrencyRates()
    try:
        fxRate = cr.get_rate(accCcy, undCcy, fxRateDate)
        return "{} {}\{} = {}".format(dateToStr(fxRateDate), accCcy, undCcy, fxRate)
    except Exception as ex:
        return "Can\'t provide Fx Rate.\n" \
               "Fx Rate {} => {} not available for Date {}".format(accCcy, undCcy, dateToStr(fxRateDate))