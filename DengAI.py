import argparse
import math
import os
import pickle
import uuid
import sys

from Accuracy_Fitness.MAE_Calc import *
from Modeling.AICc import *
from Modeling.ARIMA import *
from Modeling.Forecasting import *
from Modeling.NB import *
from Modeling.Pearson_Correlation_Coefficient import *
from Modeling.Sim_Linear_Regression import *
from Plots.Error_Plots import *
from Plots.Predict_Plots import *
from PyQt5.QtWidgets import *

class City:
    def __init__(self, name, training_features, training_labels, test_features, submissions):
        self.name = name
        self.training_features = training_features
        self.training_labels = training_labels
        self.test_labels = None
        self.test_features = test_features
        self.submissions = submissions

    def compare(self, obj):
        try:
            pandas.testing.assert_frame_equal(self.training_features, obj.training_features)
            pandas.testing.assert_frame_equal(self.training_labels, obj.training_labels)
            pandas.testing.assert_frame_equal(self.test_features, obj.test_features)
            pandas.testing.assert_frame_equal(self.submissions, obj.submissions)

            if self.test_labels is not None and obj.test_labels is not None:
                pandas.testing.assert_frame_equal(self.test_labels, obj.test_labels)
            elif self.test_labels is None != obj.test_labels is None:
                return False

            return True
        except:
            return False


def save_object(obj, name):
    filename = str(os.getcwd()) + "/temp/{}.pickle".format(name)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def get_city_uuid(city):
    directory = os.fsencode(os.getcwd() + "/temp/")
    if not os.path.isdir(directory):
        return None
    for file in os.listdir(directory):
        filename = os.fsdecode(file).split('_')
        if filename[0] == 'data' and filename[1] == city.name:
            with open(directory + file, 'br') as pickles:
                saved_city = pickle.load(pickles)
                if city.compare(saved_city):
                    return filename[2].split('.')[0]


def get_object(obj_type, city, unique_id):
    directory = os.fsencode(os.getcwd() + "/temp/")
    if not os.path.isdir(directory):
        return None
    for file in os.listdir(directory):
        filename = os.fsdecode(file).split('_')
        if filename[0] == obj_type and filename[1] == city and filename[2].split('.')[0] == unique_id:
            with open(directory + file, 'br') as pickles:
                return pickle.load(pickles)


def input_parser():
    training_features = pandas.read_csv('dengue_features_train.csv', index_col=[3])
    training_features.drop(['year', 'weekofyear'], axis=1, inplace=True)
    training_features = training_features.loc[:, ~training_features.T.duplicated(keep='first')]
    training_features.index = pandas.to_datetime(training_features.index)
    training_features.interpolate(method='time', inplace=True)

    training_labels = pandas.read_csv('dengue_labels_train.csv')
    training_labels.set_index(training_features.index, inplace=True)
    training_labels.drop(['year', 'weekofyear'], axis=1, inplace=True)

    test_features = pandas.read_csv('dengue_features_test.csv', index_col=[3])
    test_features.drop(['year', 'weekofyear'], axis=1, inplace=True)
    test_features = test_features.loc[:, ~test_features.T.duplicated(keep='first')]
    test_features.index = pandas.to_datetime(test_features.index)
    test_features.interpolate(method='time', inplace=True)

    submission = pandas.read_csv('submission_format.csv')

    cities = []

    for city in test_features['city'].drop_duplicates():
        cities.append(
            City(city, training_features[training_features['city'] == city].drop(['city'], axis=1),
                 training_labels[training_labels['city'] == city].drop(['city'], axis=1),
                 test_features[test_features['city'] == city].drop(['city'], axis=1),
                 submission[submission['city'] == city].drop(['city'], axis=1))),

    return cities


def option_parser():
    parser = argparse.ArgumentParser(description="DengAI Outbreak Modeling & Forecasting")

    group = parser.add_mutually_exclusive_group(required=True)

    # Modeling:
    group.add_argument('--sim', action='store_true', help='Simple linear regression')
    group.add_argument('--mul', action='store_true', help='Multivariable linear regression')
    parser.add_argument('--bru', action='store_true', help='Multivariable AICc bruteforce')
    group.add_argument('--ari', action='store_true', help='ARIMA Modeling')
    group.add_argument('--neu', nargs='+', help='Neural Network Modeling.')
    group.add_argument('--nb', action='store_true', help='Negative Binomial Modeling')

    # Forecast
    parser.add_argument('-F', action='store_true', help='Forecast')

    # Validation
    parser.add_argument('-V', action='store_true', help='Validation')
    parser.add_argument('--split', nargs='?', type=int, const=3, help='Splitting')
    parser.add_argument('--mae', action='store_true', help='MAE Calculation')

    # Plots
    parser.add_argument('-P', action='store_true', help='Plots')
    parser.add_argument('--err', action='store_true', help='Error')
    parser.add_argument('--pred', nargs='?', const=True, help='Predictor Plots')
    parser.add_argument('--tvo', action='store_true', help='Time vs. Outbreak Analysis')

    # Submission
    parser.add_argument('-S', action='store_true', help='Plots')
    parser.add_argument('--create', nargs='?', type=str, const="submissions_out", help='Create submission file',
                        metavar='Submission file name')

    args = parser.parse_args()
    pandas2ri.activate()
    cities = input_parser()

    # This might be able to pass to GUI
    #app = QApplication(sys.argv)
    #(options, args) = parser.parse_args(app.arguments())

    if args.bru and args.mul is None:
        parser.error("Bruteforce only works with multivariable linear modeling.")

    for city in cities:
        if args.split or args.V:
            years = city.training_features.index.drop_duplicates()
            start_year = years[math.ceil(len(years) * .7)]

            city.test_features = city.training_features[city.training_features.index >= start_year].copy(deep=True)

            city.training_features = city.training_features[city.training_features.index < start_year].copy(deep=True)

            city.test_labels = city.training_labels[city.training_labels.index >= start_year].copy(deep=True)

            city.submissions = city.training_labels[city.training_labels.index >= start_year].copy(
                deep=True).reset_index(drop=True)
            city.submissions['city'] = city.name
            city.submissions['total_cases'] = 0

            city.training_labels = city.training_labels[city.training_labels.index < start_year].copy(deep=True)

    for city in cities:
        model = None
        if args.sim:
            print("Using simple linear modeling")
            unique_id = get_city_uuid(city)
            if not unique_id:
                unique_id = str(uuid.uuid4())
                save_object(city, 'data_{}_{}'.format(city.name, unique_id))
                print('City saved')
            else:
                if args.split or args.V:
                    model = get_object('sim-split', city.name, unique_id)
                else:
                    model = get_object('sim', city.name, unique_id)

            if not model:
                predictor = pearson_correlation(city.training_features, city.training_labels)[0]
                model = simplelinearmodel(city.training_features[predictor[0]], predictor[0],
                                          city.training_labels['total_cases'])
                if args.split:
                    save_object(model, 'sim-split_{}_{}'.format(city.name, unique_id))
                else:
                    save_object(model, 'sim_{}_{}'.format(city.name, unique_id))
        if args.mul:
            print("Using multivariable linear modeling.")
            unique_id = get_city_uuid(city)
            if not unique_id:
                unique_id = str(uuid.uuid4())
                save_object(city, 'data_{}_{}'.format(city.name, unique_id))
                print('City saved')
            else:
                if args.split:
                    if args.bru:
                        model = get_object('mul-bruteforce-split', city.name, unique_id)
                    else:
                        model = get_object('mul-split', city.name, unique_id)
                else:
                    if args.bru:
                        model = get_object('mul-bruteforce', city.name, unique_id)
                    else:
                        model = get_object('mul', city.name, unique_id)
                        print(model)
            if not model:
                if args.bru:
                    model = bruteforce_AICc(city.training_features, city.training_labels['total_cases'])
                    if args.split:
                        save_object(model, 'mul-bruteforce-split_{}_{}'.format(city.name, unique_id))
                    else:
                        save_object(model, 'mul-bruteforce_{}_{}'.format(city.name, unique_id))
                else:
                    model = AICc(city.training_features, city.training_labels['total_cases'])
                    if args.split:
                        save_object(model, 'mul-split_{}_{}'.format(city.name, unique_id))
                    else:
                        save_object(model, 'mul_{}_{}'.format(city.name, unique_id))
        if args.ari:
            print("Implementing ARIMA errors.")
            unique_id = get_city_uuid(city)
            if not unique_id:
                unique_id = str(uuid.uuid4())
                save_object(city, 'data_{}_{}'.format(city.name, unique_id))
                print('City saved')
            else:
                if args.split or args.V:
                    model = get_object('ari-split', city.name, unique_id)
                else:
                    model = get_object('ari', city.name, unique_id)

            if not model:
                model = ARIMA_seasonal(city.training_features, city.training_labels)

                if args.split or args.V:
                    save_object(model, 'ari-split_{}_{}'.format(city.name, unique_id))
                else:
                    save_object(model, 'ari_{}_{}'.format(city.name, unique_id))
        if args.nb:
            print("Using NB modeling.")
            unique_id = get_city_uuid(city)
            if not unique_id:
                unique_id = str(uuid.uuid4())
                save_object(city, 'data_{}_{}'.format(city.name, unique_id))
                print('City saved')
            else:
                if args.split or args.V:
                    model = get_object('nb-split', city.name, unique_id)
                    fourier_terms = get_object('nb-split-fourier', city.name, unique_id)
                else:
                    model = get_object('nb', city.name, unique_id)
                    fourier_terms = get_object('nb-fourier', city.name, unique_id)

            if not model or not fourier_terms:
                model, fourier_terms = NB(city.training_features, city.training_labels)
                if args.split or args.V:
                    save_object(model, 'nb-split_{}_{}'.format(city.name, unique_id))
                    save_object(fourier_terms, 'nb-split-fourier_{}_{}'.format(city.name, unique_id))
                else:
                    save_object(model, 'nb_{}_{}'.format(city.name, unique_id))
                    save_object(fourier_terms, 'nb-fourier_{}_{}'.format(city.name, unique_id))
        if args.neu:
            print("Using Neural network modeling.")
        if args.create or args.split or args.V:
            if args.nb:
                fcast = forecast(model, city.test_features, fourier_terms)
            else:
                fcast = forecast(model, city.test_features)

            if args.ari:
                total_cases = fcast[3]
            else:
                fcast = forecast(model, city.test_features)

            for i in range(0, len(fcast[1])):
                if fcast[1][i] < 0:
                    city.submissions.loc[i, 'total_cases'] = 0
                else:
                    city.submissions.loc[i, 'total_cases'] = round(total_cases[i])
        if args.pred:
            print("Predictor plots for multivariable linear regression")
            for i in robjects.r['all.vars'](robjects.r['terms'](model))[1:]:
                corr_plot(city.training_features[i], i, city.training_labels['total_cases'], 'Total Cases',
                          '{} vs. Total Cases for {}'.format(i, city.name))
        if args.mae or args.V:
            print("Calculating MAE")
            mae(city.submissions['total_cases'], city.test_labels['total_cases'])
        if args.err or args.V:
            print("Error plots.")
            # Plots.Error_Plots >> error_plot(week, predicted_values, actual_values, city)
            error_plot(city.test_labels.index, city.submissions['total_cases'],
                       city.test_labels['total_cases'], city.name)
        if args.create:
            print("Create submission file")
            df_array = []
            for city in cities:
                df_array.append(city.submissions)
            pandas.concat(df_array).to_csv("{}.csv".format(args.create), index=False)

    plt.show()


#def main():
    #option_parser()


#main()
