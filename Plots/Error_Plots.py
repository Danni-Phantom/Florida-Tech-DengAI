import matplotlib.pyplot as plt


def error_plot(week, prediction, actual, city):

    diff = []
    for x in range(0, len(prediction)):
        diff.append(prediction[x] - actual[x])

    plt.figure()
    plt.scatter(week, diff, label='Error')
    plt.scatter(week, prediction, label='Prediction')
    plt.scatter(week, actual, label='Actual')
    plt.xlabel("Date")
    plt.ylabel("Difference")
    plt.title("Error Plot for {}".format(city))
    plt.legend()
    plt.plot()
