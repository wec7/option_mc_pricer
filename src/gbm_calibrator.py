from functools import lru_cache

import numpy as np
from singleton_decorator import singleton

from data_loader import DataLoader


@singleton
class GBMCalibrator(object):

    @lru_cache(None)
    def calibration(self, ticker):
        # bring data
        data = DataLoader().load_equity(ticker)
        r = np.log(data['Adj_Close']).diff().as_matrix()[1:]

        # estimate parameters
        sigma = np.std(r)
        mu = np.mean(r) + 0.5 * sigma * sigma

        return mu, sigma

    def calibrated_sigma(self, ticker):
        return self.calibration(ticker)[1]

    def calibrated_mu(self, ticker):
        return self.calibration(ticker)[0]


if __name__ == '__main__':
    print(GBMCalibrator().calibrated_sigma('MSFT'))
    print(GBMCalibrator().calibrated_mu('MSFT'))
