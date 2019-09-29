import rpy2.robjects as robjects
import pandas
from rpy2.robjects.packages import importr

fcast_package = importr('forecast')

def ARIMA(features, dengue):
    model = fcast_package.auto_arima(dengue, xreg=robjects.r['as.matrix'](features))
    return model


def ARIMA_seasonal(features, dengue):
    model = fcast_package.stlm(robjects.r['ts'](dengue, frequency=52), xreg=robjects.r['ts'](features, frequency=52),
                               method='arima', stepwise=False, approximation=False, ic='bic')
    return model
