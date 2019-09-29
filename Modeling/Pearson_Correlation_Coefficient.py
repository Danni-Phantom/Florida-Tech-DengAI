import rpy2.robjects as robjects


def pearson_correlation(features, labels):
    coefficient_list = []
    for predictor in list(features):
        coefficient = \
        robjects.r['cor'](features[predictor], labels['total_cases'], method="pearson", use="complete.obs")[0]
        coefficient_list.append((predictor, abs(coefficient)))
    coefficient_list.sort(key=lambda x: x[1], reverse=True)

    # Add option to select top n

    return coefficient_list
