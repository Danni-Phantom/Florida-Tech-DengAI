import unittest

from rpy2.robjects import pandas2ri
pandas2ri.activate()
import sys

from Modeling.AICc import *

X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

X2 = [737, 311, 511, 156, 201, 423, 412, 134, 487, 609, 312, 300, 346, 971, 641, 581, 812, 872, 846, 706, 403, 178,
      986, 168, 432]

Y = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]

AICc_TESTFEATURES = {
    'X': X,
    'X2': X2
}

AICc_TESTLABELS = {
    'total_cases': Y
}

AICc_TESTFEATURESDF = pandas.DataFrame(AICc_TESTFEATURES)
AICc_TESTLABELSDF = pandas.DataFrame(AICc_TESTLABELS)


class test_AICc(unittest.TestCase):

    def test_AICc(self):
        model = AICc(AICc_TESTFEATURESDF, AICc_TESTLABELSDF['total_cases'])
        predictors = model.rx2('coefficients')

        self.assertIs(len(predictors), 3)
        self.assertLess(abs(predictors[2]), sys.float_info.epsilon)
        self.assertEqual(predictors.names[1], 'X')
        self.assertEqual(predictors.names[2], 'X2')

    def test_bruteforce_AICc(self):
        model = bruteforce_AICc(AICc_TESTFEATURESDF, AICc_TESTLABELSDF['total_cases'])
        predictors = model.rx2('coefficients')

        self.assertEqual(len(predictors), 3)
        self.assertLess(abs(predictors[2]), sys.float_info.epsilon)
        self.assertEqual(predictors.names[1], 'X')
        self.assertEqual(predictors.names[2], 'X2')

    if __name__ == '__main__':
        unittest.main()
