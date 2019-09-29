# from rpy2 import robjects
# from rpy2.robjects.packages import STAP
# from rpy2.robjects.packages import importr
# from tqdm import tqdm
#
# glmulti_package = importr('glmulti')
# fcast_package = importr('forecast')
#
#
# def NB(features, dengue):
#     glm_redefined = STAP(
#         "glm.redefined = function(formula, data, always=\"\", ...){ glm.nb(as.formula"
#         "(paste(deparse(formula), always)), data=data, ...)}", "redefined_glm")
#     optimal_score = float("inf")
#     optimal_model = None
#     optimal_fourier = None
#     optimal_k = 0
#     for k in tqdm(range(1, 2)):
#         fourier_terms = robjects.r['as.data.frame'](
#             fcast_package.fourier(robjects.r['ts'](dengue['total_cases'], frequency=52), K=k))
#         fourier_terms.names = [x.replace('-', '_') for x in fourier_terms.names]
#         model = glmulti_package.glmulti(y='total_cases ~ ' + ("+".join(list(features))), method='g',
#                                         fitfunc=glm_redefined.glm_redefined,
#                                         data=robjects.r['cbind'](fourier_terms, dengue, features), level=1,
#                                         plotty=False,
#                                         report=False, always='+' + "+".join(fourier_terms.names))
#         AICc_score = robjects.r['summary'](model )[7][0]
#         if AICc_score < optimal_score:
#             optimal_score = AICc_score
#             optimal_model = model
#             optimal_fourier = fourier_terms
#             optimal_k = k
#         del model
#         del fourier_terms
#     print(optimal_k)
#     return optimal_model, optimal_fourier
