import rpy2.robjects as robjects
from rpy2.robjects import Formula


def simplelinearmodel(predictor, name, dengue):
    fmla = Formula('dengue ~ {}'.format(name))
    env = fmla.environment
    env[name] = predictor
    env['dengue'] = dengue
    return robjects.r('lm(%s)' % fmla.r_repr())
