from contexttimer import Timer

from pricing import EuropeanVanillaPricing


class Parameters:
    pass


if __name__ == '__main__':
    testParam = Parameters()
    testParam.T = 1.0
    testParam.S = 90.0
    testParam.K = 100.0
    testParam.sigma = 0.15
    testParam.r = 0.05
    testParam.method = 'mc'
    testParam.pc = 'call'
    testParam.iterations = 1000000

    option = EuropeanVanillaPricing(testParam)
    print('Method: Monte Carlo')
    with Timer() as t:
        print('MC Price: %s' % option.get_price())
        print('BS Price: %s' % option.get_mc_price())

    print('Iterations: %s' % testParam.iterations)
    print('Time Taken: %ss' % t.elapsed)
