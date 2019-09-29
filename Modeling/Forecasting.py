from rpy2 import robjects
from rpy2.robjects.packages import importr

fcast_package = importr('forecast')


def forecast(model, features, fourier_terms=None):
    if fourier_terms:
        return robjects.r['predict'](model, newdata=robjects.r['cbind'](features,
                                                                        fourier_terms.rx(robjects.IntVector(
                                                                            range(1, len(features) + 1)), True)),
                                     type='response')
    else:
        return fcast_package.forecast(model, newdata=features, xreg=features.to_numpy())
