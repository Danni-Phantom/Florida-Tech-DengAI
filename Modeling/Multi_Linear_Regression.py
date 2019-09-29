import rpy2.robjects as robjects
import pandas


def multivariable_linear_model(features, predictors, dengue):
    fmla = ''
    temp = [dengue]
    for predictor in predictors:
        fmla = ''.join([fmla, predictor, ' + '])
        temp.append(features[predictor])
    # Remove last ' + '
    fmla = fmla[:-3]
    fmla = 'total_cases ~ {}'.format(fmla)

    model = robjects.r.lm(fmla, data=pandas.concat(temp, axis=1))
    del temp
    return model
