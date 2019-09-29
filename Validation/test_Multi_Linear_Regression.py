import unittest

import pandas
from rpy2.robjects import pandas2ri

from Modeling.Multi_Linear_Regression import *

TESTINTERCEPT = 111.4
TEST_X_SLOPE = 2.06
TEST_X2_SLOPE = -2.73
TEST_X3_SLOPE = .001

X = [81.69, 103.84, 96.54, 95.15, 92.88, 99.13, 85.43, 90.49, 95.55, 83.39, 107.95, 92.41, 85.65, 87.89, 86.54, 85.22,
     94.51, 80.80, 88.91, 90.59, 79.06, 95.50, 83.18, 93.55, 79.86, 106.25, 79.35, 86.67, 85.78, 94.96, 99.79, 88.00,
     83.43, 94.81, 94.94, 89.40, 93.00, 93.59]

X2 = [64.5, 73.3, 68.8, 65.0, 69.0, 64.5, 66.0, 66.3, 68.8, 64.5, 70.0, 69.0, 70.5, 66.0, 68.0, 68.5, 73.5, 66.3, 70.0,
      76.5, 62.0, 68.0, 63.0, 72.0, 68.0, 77.0, 63.0, 66.5, 62.5, 67.0, 75.5, 69.0, 66.5, 66.5, 70.5, 64.5, 74.0, 75.5]

X3 = [118, 143, 172, 147, 146, 138, 175, 134, 172, 118, 151, 155, 155, 146, 135, 127, 178, 136, 180, 186, 122, 132, 114,
      171, 140, 187, 106, 159, 127, 191, 192, 181, 143, 153, 144, 139, 148, 179]

Y = [124, 150, 128, 134, 110, 131, 98, 84, 147, 124, 128, 124, 147, 90, 96, 120, 102, 84, 86, 84, 134, 128, 102, 131,
     84, 110, 72, 124, 132, 137, 110, 86, 81, 128, 124, 94, 74, 89]

MULTI_LINEAR_TESTFEATURES = {
    'city': ['test'] * len(X),
    'year': X,
    'weekofyear': X,
    'week_start_date': X,
    'X': X,
    'X2': X2,
    'X3': X3
}

MULTI_LINEAR_TESTLABELS = {
    'city': ['test'] * len(X),
    'year': Y,
    'weekofyear': Y,
    'total_cases': Y
}

MULTI_LINEAR_TESTFEATURESDF = pandas.DataFrame(MULTI_LINEAR_TESTFEATURES)
MULTI_LINEAR_TESTLABELSDF = pandas.DataFrame(MULTI_LINEAR_TESTLABELS)


class test_Multi_Linear_Regression(unittest.TestCase):

    def test_Multi_Linear_Regression(self):
        pandas2ri.activate()
        model = multivariable_linear_model(MULTI_LINEAR_TESTFEATURESDF, ['X', 'X2', 'X3'],
                                           MULTI_LINEAR_TESTLABELSDF['total_cases'])

        self.assertLess(abs(model.rx2('coefficients')[0] - round(TESTINTERCEPT, 1)), .1)
        self.assertLess(abs(model.rx2('coefficients')[1] - round(TEST_X_SLOPE, 2)), .01)
        self.assertLess(abs(model.rx2('coefficients')[2] - round(TEST_X2_SLOPE, 2)), .01)
        self.assertLess(abs(model.rx2('coefficients')[3] - round(TEST_X3_SLOPE, 3)), .001)

    if __name__ == '__main__':
        unittest.main()
