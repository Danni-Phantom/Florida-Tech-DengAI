import numpy as np


def mae(prediction, actual):
    diff = []
    for x in range(0, len(prediction)):
        diff.append(np.abs(prediction[x] - actual[x]))

    mean = np.mean(diff)
    print("MAE = " + str(mean))
