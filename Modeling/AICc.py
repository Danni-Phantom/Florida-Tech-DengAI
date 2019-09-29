import itertools as it

from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr
from tqdm import tqdm

from Modeling.Multi_Linear_Regression import *

fcast_package = importr('forecast')
mass_package = importr('MASS')
imputeTS_package = importr('imputeTS')


def powerset(iterable):
    s = list(iterable)
    return it.chain.from_iterable(it.combinations(s, r) for r in range(len(s) + 1))


def AICc(features, labels):
    pandas2ri.activate()
    predictors = list(features)

    model = multivariable_linear_model(features, predictors, labels)
    optimal_model = mass_package.stepAIC(model, direction="both", trace=False)

    return optimal_model


def bruteforce_AICc(features, labels):
    pandas2ri.activate()
    predictors = list(features)

    # Remove the empty set.
    combination_predictors = list(powerset(predictors))[1:]

    optimal_score = float("inf")
    optimal_model = None

    for x in tqdm(combination_predictors):
        model = multivariable_linear_model(features, x, labels)
        AICc_score = fcast_package.CV(model).rx(3)[0]
        if AICc_score < optimal_score:
            optimal_score = AICc_score
            optimal_model = model
    return optimal_model
