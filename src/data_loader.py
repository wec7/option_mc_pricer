import configparser
from functools import lru_cache

import quandl
from singleton_decorator import singleton

config = configparser.ConfigParser()
config.read('../config/quandl.ini')


@singleton
class DataLoader(object):

    def __init__(self, start_date="2018-01-01", end_date="2018-05-20"):
        self.start_date = start_date
        self.end_date = end_date

    @lru_cache(None)
    def load_equity(self, ticker):
        return quandl.get(
            "EOD/%s" % ticker,
            authtoken=config['quandl.com']['authtoken'],
            start_date=self.start_date,
            end_date=self.end_date
        )

    @lru_cache(None)
    def load_rate(self, date):
        series = quandl.get(
            "USTREASURY/YIELD",
            authtoken=config['quandl.com']['authtoken'],
            start_date=date,
            end_date=date,
        ).loc[date]
        series.index = map(int, dict(config['quandl rates index']).values())
        return series / 100


if __name__ == '__main__':
    import datetime
    print(DataLoader().load_rate(datetime.datetime(2018, 5, 18)))
