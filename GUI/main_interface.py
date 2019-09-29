from PyQt5.QtWidgets import *
import pandas
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from GUI.main_gui import *
from PyQt5.QtChart import *
from Accuracy_Fitness import MAE_Calc
from GUI.main_gui import Ui_DengAI

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt


# import sys
# import DengAI
# import argparse
# import argparseui
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
# import numpy as np


class Communicate(QObject):

    closeApp = pyqtSignal()


class City:
    def __init__(self, name, training_features, training_labels, test_features, submissions):
        self.name = name
        self.training_features = training_features
        self.training_labels = training_labels
        self.test_labels = None
        self.test_features = test_features
        self.submissions = submissions

class MainWindow(QMainWindow, Ui_DengAI):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.c = Communicate()
        self.c.closeApp.connect(self.close)
        self.setWindowTitle('DengAI')

        #self.Setup_Window()
        self.Setup_Home()
        self.Setup_DataSet()
        self.Setup_Predictor()
        self.Setup_Algorithm()
        self.Setup_Evaluation()
        self.Setup_Analysis()

    #def Setup_Window(self):

    def Setup_Home(self):
        # Home Tab #

        # Button to move to Next Tab: Data Sets
        self.b_Get_Started = QPushButton("Get Started!", self.Home_tab)
        self.b_Get_Started.setGeometry(QRect(350, 310, 114, 32))
        self.b_Get_Started.setObjectName("b_Get_Started")
        self.b_Get_Started.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.DataSets_tab))

        # Text Box to display intro to the Program
        self.t_Intro = QTextBrowser(self.Home_tab)
        self.t_Intro.setGeometry(QRect(430, 60, 371, 201))
        self.t_Intro.setObjectName("t_Intro")
        self.t_Intro.setHtml(
            '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'.SF NS Text'; font-size:13pt; font-weight:400; font-style:normal;\><p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=" font-family:'Helvetica Neue';">DengAI is a program that's goal is to predict the outbreak of Dengue Fever based on climate data. This disease is spread by mosquitos and has had outbreaks all over the world. Acording to the CDC as many as 400 million people are infected yearly and 40% of the world's population live in areas where there is a risk for dengue transmission.  The World Health organization, also known as WHO, has estimated as many as 22,000 people die anually. It is our hope that by predicting the number of outbreaks an area may expirence, the proper resources and aid can be given to that area before an epidemic happens. </span></p></body></html>''')

        # Image of Mosquito eating Man

        # self.p_Mosquito = QGraphicsView(self.Home_tab)
        # self.p_Mosquito.setGeometry(QRect(50, 60, 291, 201))
        # self.p_Mosquito.setObjectName("p_Mosquito")

    def Setup_DataSet(self):
        # Button to move to Next Tab: Predictors
        self.b_Next_datasets = QtWidgets.QPushButton(self.DataSets_tab)
        self.b_Next_datasets.setGeometry(QtCore.QRect(670, 350, 114, 32))
        self.b_Next_datasets.setObjectName("b_Next_datasets")
        self.b_Next_datasets.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.Predictors_tab))
        self.b_Next_datasets.setText("Next")

        #Radio Buttons
        self.r_Testing_Data = QtWidgets.QRadioButton(self.DataSets_tab)
        self.r_Testing_Data.setGeometry(QtCore.QRect(60, 100, 100, 16))
        self.r_Testing_Data.setObjectName("r_Testing_Data")
        self.r_Testing_Data.setText("Testing Data")

        self.r_Training_Data = QtWidgets.QRadioButton(self.DataSets_tab)
        self.r_Training_Data.setGeometry(QtCore.QRect(60, 122, 100, 16))
        self.r_Training_Data.setObjectName("r_Training_Data")
        self.r_Training_Data.setText("Training Data")

        self.r_Other = QtWidgets.QRadioButton(self.DataSets_tab)
        self.r_Other.setGeometry(QtCore.QRect(60, 145, 100, 16))
        self.r_Other.setObjectName("r_Other")
        self.r_Other.setText("Other")

        #Instructions
        self.lab_Instruct_dataSets = QtWidgets.QLabel(self.DataSets_tab)
        self.lab_Instruct_dataSets.setGeometry(QtCore.QRect(60, 20, 731, 61))
        self.lab_Instruct_dataSets.setObjectName("lab_Instruct_dataSets")
        self.lab_Instruct_dataSets.setText("Please select a CSV file to import or select one of the pre loaded datasets. The data given was provided by DrivenData in \n"
                                           " conjunction with the CDC for the cities of San Jan and Iquitos. ")

        # File location label
        self.lab_fileLoc = QtWidgets.QLabel(self.DataSets_tab)
        self.lab_fileLoc.setGeometry(QtCore.QRect(70, 180, 57, 10))
        self.lab_fileLoc.setObjectName("lab_fileLoc")
        self.lab_fileLoc.setText("/")

        # Button to select file
        self.b_File = QtWidgets.QPushButton(self.DataSets_tab)
        self.b_File.setGeometry(QtCore.QRect(60, 200, 114, 32))
        self.b_File.setObjectName("b_File")
        # TODO: WTF is lambda
        self.b_File.clicked.connect(lambda: self.openFile())
        self.b_File.setText("File...")

    def Setup_Predictor(self):

        #self.QApplication.arguments().append("--pred")

        self.c_Precip_mm = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Precip_mm.setGeometry(QtCore.QRect(80, 220, 131, 20))
        self.c_Precip_mm.setObjectName("c_Precip_mm")
        self.c_Precip_mm.setText("Precipitation (mm)")
        # if self.c_Precip_mm.setChecked(True):
        #     self.QApplication.arguments().append("precipitation_amt_mm")
        # elif self.c_Precip_mm.setChecked(False):
        #     self.QApplication.arguments().


        self.c_TDTR = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_TDTR.setGeometry(QtCore.QRect(260, 200, 85, 20))
        self.c_TDTR.setObjectName("c_TDTR")
        self.c_TDTR.setText("TDTR (K)")

        self.c_Air_Temp = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Air_Temp.setGeometry(QtCore.QRect(80, 240, 141, 20))
        self.c_Air_Temp.setObjectName("c_Air_Temp")
        self.c_Air_Temp.setText("Air Temperature (K)")

        self.c_City = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_City.setGeometry(QtCore.QRect(80, 60, 85, 20))
        self.c_City.setObjectName("c_City")
        self.c_City.setText("City")

        self.c_Sta_Precip = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Sta_Precip.setGeometry(QtCore.QRect(500, 100, 181, 20))
        self.c_Sta_Precip.setObjectName("c_Sta_Precip")
        self.c_Sta_Precip.setText("Station Precipitation (mm)")

        self.c_Sat_Precip = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Sat_Precip.setGeometry(QtCore.QRect(260, 160, 201, 20))
        self.c_Sat_Precip.setObjectName("c_Sat_Precip")
        self.c_Sat_Precip.setText("Saturation Precipitation (mm)")

        self.c_Week_Of_Year = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Week_Of_Year.setGeometry(QtCore.QRect(80, 100, 101, 20))
        self.c_Week_Of_Year.setObjectName("c_Week_Of_Year")
        self.c_Week_Of_Year.setText("Week of Year")

        self.c_NDVI_SW = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_NDVI_SW.setGeometry(QtCore.QRect(80, 200, 85, 20))
        self.c_NDVI_SW.setObjectName("c_NDVI_SW")
        self.c_NDVI_SW.setText("NDVI (SW)")

        self.c_NDVI_NE = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_NDVI_NE.setGeometry(QtCore.QRect(80, 140, 85, 20))
        self.c_NDVI_NE.setObjectName("c_NDVI_NE")
        self.c_NDVI_NE.setText("NDVI (NE)")

        self.c_Spec_Hum = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Spec_Hum.setGeometry(QtCore.QRect(260, 180, 161, 20))
        self.c_Spec_Hum.setObjectName("c_Spec_Hum")
        self.c_Spec_Hum.setText("Specific Humidity (g/kg)")

        self.c_Sta_Avg_Temp = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Sta_Avg_Temp.setGeometry(QtCore.QRect(260, 220, 211, 20))
        self.c_Sta_Avg_Temp.setObjectName("c_Sta_Avg_Temp")
        self.c_Sta_Avg_Temp.setText("Station Average Temperature (C)")

        self.c_Max_Air_Temp = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Max_Air_Temp.setGeometry(QtCore.QRect(260, 80, 171, 20))
        self.c_Max_Air_Temp.setObjectName("c_Max_Air_Temp")
        self.c_Max_Air_Temp.setText("Max Air Temperature (K)")

        self.c_Rel_Hum = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Rel_Hum.setGeometry(QtCore.QRect(260, 140, 161, 20))
        self.c_Rel_Hum.setObjectName("c_Rel_Hum")
        self.c_Rel_Hum.setText("Relative Humidity (%)")

        self.c_NDVI_SE = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_NDVI_SE.setGeometry(QtCore.QRect(80, 180, 85, 20))
        self.c_NDVI_SE.setObjectName("c_NDVI_SE")
        self.c_NDVI_SE.setText("NDVI (SE)")

        self.c_Sta_DUIR_Temp_Rang = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Sta_DUIR_Temp_Rang.setGeometry(QtCore.QRect(260, 240, 241, 20))
        self.c_Sta_DUIR_Temp_Rang.setObjectName("c_Sta_DUIR_Temp_Rang")
        self.c_Sta_DUIR_Temp_Rang.setText("Station DIUR Temperature Range (C)")

        self.c_Year = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Year.setGeometry(QtCore.QRect(80, 80, 85, 20))
        self.c_Year.setObjectName("c_Year")
        self.c_Year.setText("Year")

        self.c_Dew_Point_Temp = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Dew_Point_Temp.setGeometry(QtCore.QRect(260, 60, 181, 20))
        self.c_Dew_Point_Temp.setObjectName("c_Dew_Point_Temp")
        self.c_Dew_Point_Temp.setText("Dew Point Temperature (K)")

        self.c_Week_Start_Date = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Week_Start_Date.setGeometry(QtCore.QRect(80, 120, 121, 20))
        self.c_Week_Start_Date.setObjectName("c_Week_Start_Date")
        self.c_Week_Start_Date.setText("Week Start Date")

        self.c_Precip_kg_per_m2 = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Precip_kg_per_m2.setGeometry(QtCore.QRect(260, 120, 151, 20))
        self.c_Precip_kg_per_m2.setObjectName("c_Precip_kg_per_m2")
        self.c_Precip_kg_per_m2.setText("Precipitation (kg/m^2)")

        self.c_Min_Air_Temp = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Min_Air_Temp.setGeometry(QtCore.QRect(260, 100, 191, 20))
        self.c_Min_Air_Temp.setObjectName("c_Min_Air_Temp")
        self.c_Min_Air_Temp.setText("Minimum Air Temperature (K)")

        self.c_Sta_Max_Temp = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Sta_Max_Temp.setGeometry(QtCore.QRect(500, 60, 201, 20))
        self.c_Sta_Max_Temp.setObjectName("c_Sta_Max_Temp")
        self.c_Sta_Max_Temp.setText("Station Max Temperature (C)")

        self.c_Sta_Min_Temp = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_Sta_Min_Temp.setGeometry(QtCore.QRect(500, 80, 221, 20))
        self.c_Sta_Min_Temp.setObjectName("c_Sta_Min_Temp")
        self.c_Sta_Min_Temp.setText("Station Minimum Temperature (C)")

        self.c_NDVI_NW = QtWidgets.QCheckBox(self.Predictors_tab)
        self.c_NDVI_NW.setGeometry(QtCore.QRect(80, 160, 85, 20))
        self.c_NDVI_NW.setObjectName("c_NDVI_NW")
        self.c_NDVI_NW.setText("NDVI (NW)")

        self.lab_Instruct_Predictors = QtWidgets.QLabel(self.Predictors_tab)
        self.lab_Instruct_Predictors.setGeometry(QtCore.QRect(70, 20, 631, 16))
        self.lab_Instruct_Predictors.setObjectName("lab_Instruct_Predictors")
        self.lab_Instruct_Predictors.setText("Please select the predictors that you wish to be used to create a prediction of how many cases will happen")

        self.b_Select = QtWidgets.QPushButton(self.Predictors_tab)
        self.b_Select.setGeometry(QtCore.QRect(500, 160, 81, 32))
        self.b_Select.setObjectName("b_Select")
        self.b_Select.setText("Select All")
        self.b_Select.clicked.connect(lambda: selectAll(self))

        self.b_deselect = QtWidgets.QPushButton(self.Predictors_tab)
        self.b_deselect.setGeometry(QtCore.QRect(570, 160, 111, 32))
        self.b_deselect.setObjectName("b_deselect")
        self.b_deselect.setText("Deselect All")
        self.b_deselect.clicked.connect(lambda: deselectAll(self))

        self.comboBox_city = QtWidgets.QComboBox(self.Predictors_tab)
        self.comboBox_city.setGeometry(QtCore.QRect(560, 120, 91, 40))
        self.comboBox_city.setObjectName("comboBox_city")
        self.comboBox_city.addItem("")
        self.comboBox_city.addItem("")
        self.comboBox_city.setItemText(0, "iq")
        self.comboBox_city.setItemText(1, "sj")

        self.lab_city = QtWidgets.QLabel(self.Predictors_tab)
        self.lab_city.setGeometry(QtCore.QRect(500, 130, 57, 16))
        self.lab_city.setObjectName("lab_city")
        self.lab_city.setText("City:")

        self.b_Previous = QtWidgets.QPushButton(self.Predictors_tab)
        self.b_Previous.setGeometry(QtCore.QRect(530, 270, 114, 32))
        self.b_Previous.setObjectName("b_Previous")
        self.b_Previous.setText("Previous")
        self.b_Previous.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.DataSets_tab))

        self.b_Next_Predictors = QtWidgets.QPushButton(self.Predictors_tab)
        self.b_Next_Predictors.setGeometry(QtCore.QRect(650, 270, 114, 32))
        self.b_Next_Predictors.setObjectName("b_Next_Predictors")
        self.b_Next_Predictors.setText("Next")
        self.b_Next_Predictors.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.Algorithm_tab))

    def Setup_Algorithm(self):

        self.b_Previous_Algorithm = QtWidgets.QPushButton(self.Algorithm_tab)
        self.b_Previous_Algorithm.setGeometry(QtCore.QRect(560, 360, 114, 32))
        self.b_Previous_Algorithm.setObjectName("b_Previous_Algorithm")
        self.b_Previous_Algorithm.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.Predictors_tab))
        self.b_Previous_Algorithm.setText("Previous")

        self.b_Next_Algorithm = QtWidgets.QPushButton(self.Algorithm_tab)
        self.b_Next_Algorithm.setGeometry(QtCore.QRect(680, 360, 114, 32))
        self.b_Next_Algorithm.setObjectName("b_Next_Algorithm")
        self.b_Next_Algorithm.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.Evaluation_tab))
        self.b_Next_Algorithm.setText("Next")

        self.c_prev_data = QtWidgets.QCheckBox(self.Algorithm_tab)
        self.c_prev_data.setGeometry(QtCore.QRect(60, 260, 281, 20))
        self.c_prev_data.setObjectName("c_prev_data")
        self.c_prev_data.setText( "Use previous data to make faster prediction")

        self.lab_Instruct_Algoritm = QtWidgets.QLabel(self.Algorithm_tab)
        self.lab_Instruct_Algoritm.setGeometry(QtCore.QRect(60, 20, 661, 31))
        self.lab_Instruct_Algoritm.setObjectName("lab_Instruct_Algoritm")
        self.lab_Instruct_Algoritm.setText("Please select an Algorithm to use to predict the outbreaks. For more information on each algorithm,\n"
                                           "visit the project site")

        self.frame_predictors_algorithm = QtWidgets.QFrame(self.Algorithm_tab)
        self.frame_predictors_algorithm.setGeometry(QtCore.QRect(60, 80, 211, 171))
        self.frame_predictors_algorithm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_predictors_algorithm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_predictors_algorithm.setObjectName("frame_predictors_algorithm")

        self.r_BICc = QtWidgets.QRadioButton(self.frame_predictors_algorithm)
        self.r_BICc.setGeometry(QtCore.QRect(10, 80, 97, 20))
        self.r_BICc.setObjectName("r_BICc")
        self.r_BICc.setText("BICc")

        self.r_AICc = QtWidgets.QRadioButton(self.frame_predictors_algorithm)
        self.r_AICc.setGeometry(QtCore.QRect(10, 40, 97, 20))
        self.r_AICc.setObjectName("r_AICc")
        self.r_AICc.setText("AICc")

        self.r_Pearson = QtWidgets.QRadioButton(self.frame_predictors_algorithm)
        self.r_Pearson.setGeometry(QtCore.QRect(10, 60, 97, 20))
        self.r_Pearson.setObjectName("r_Pearson")
        self.r_Pearson.setText("Pearson")

        self.lab_pred_select = QtWidgets.QLabel(self.frame_predictors_algorithm)
        self.lab_pred_select.setGeometry(QtCore.QRect(10, 10, 181, 16))
        self.lab_pred_select.setObjectName("lab_pred_select")
        self.lab_pred_select.setText("Predictor Selection Algorithm")

        self.frame_model_algorithms = QtWidgets.QFrame(self.Algorithm_tab)
        self.frame_model_algorithms.setGeometry(QtCore.QRect(310, 80, 211, 171))
        self.frame_model_algorithms.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_model_algorithms.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_model_algorithms.setObjectName("frame_model_algorithms")

        self.r_Arima = QtWidgets.QRadioButton(self.frame_model_algorithms)
        self.r_Arima.setGeometry(QtCore.QRect(10, 80, 61, 20))
        self.r_Arima.setObjectName("r_Arima")
        self.r_Arima.setText("Arima")

        self.r_Sing_Var_Reg = QtWidgets.QRadioButton(self.frame_model_algorithms)
        self.r_Sing_Var_Reg.setGeometry(QtCore.QRect(10, 40, 181, 20))
        self.r_Sing_Var_Reg.setObjectName("r_Sing_Var_Reg")
        self.r_Sing_Var_Reg.setText("Single Variable Regression")

        self.r_Mult_Var_Reg = QtWidgets.QRadioButton(self.frame_model_algorithms)
        self.r_Mult_Var_Reg.setGeometry(QtCore.QRect(10, 60, 171, 20))
        self.r_Mult_Var_Reg.setObjectName("r_Mult_Var_Reg")
        self.r_Mult_Var_Reg.setText("Multivariable Regression")

        self.r_Multi_AICc_brute = QtWidgets.QRadioButton(self.frame_model_algorithms)
        self.r_Multi_AICc_brute.setGeometry(QtCore.QRect(10, 100, 191, 20))
        self.r_Multi_AICc_brute.setObjectName("r_Multi_AICc_brute")
        self.r_Multi_AICc_brute.setText("Multivariable AICc bruteforce")

        self.r_NNModeling = QtWidgets.QRadioButton(self.frame_model_algorithms)
        self.r_NNModeling.setGeometry(QtCore.QRect(10, 120, 181, 20))
        self.r_NNModeling.setObjectName("r_NNModeling")
        self.r_NNModeling.setText("Neural Network Modeling")

        self.r_PAR_Modeling = QtWidgets.QRadioButton(self.frame_model_algorithms)
        self.r_PAR_Modeling.setGeometry(QtCore.QRect(10, 140, 111, 20))
        self.r_PAR_Modeling.setObjectName("r_PAR_Modeling")
        self.r_PAR_Modeling.setText("PAR Modeling")

        self.lab_alg_select = QtWidgets.QLabel(self.frame_model_algorithms)
        self.lab_alg_select.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.lab_alg_select.setObjectName("lab_alg_select")
        self.lab_alg_select.setText("Modeling Algorithm")

    def Setup_Evaluation(self):
        self.b_Back_Evaluation = QtWidgets.QPushButton(self.Evaluation_tab)
        self.b_Back_Evaluation.setGeometry(QtCore.QRect(560, 400, 114, 32))
        self.b_Back_Evaluation.setObjectName("b_Back_Evaluation")
        self.b_Back_Evaluation.setText("Back")
        self.b_Back_Evaluation.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.Algorithm_tab))

        self.b_AnalyzeTheData = QtWidgets.QPushButton(self.Evaluation_tab)
        self.b_AnalyzeTheData.setGeometry(QtCore.QRect(683, 400, 131, 32))
        self.b_AnalyzeTheData.setObjectName("b_AnalyzeTheData")
        self.b_AnalyzeTheData.setText("Analyze the Data")
        self.b_AnalyzeTheData.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.Analysis_tab))

        self.t_MAE_Number = QtWidgets.QTextBrowser(self.Evaluation_tab)
        self.t_MAE_Number.setGeometry(QtCore.QRect(90, 10, 91, 30))
        self.t_MAE_Number.setObjectName("t_MAE_Number")
        self.t_MAE_Number.setText("33.68")

        self.g_EvaluationGraph = QWidget(self.Evaluation_tab)
        self.g_EvaluationGraph.setGeometry(QtCore.QRect(200, 10, 591, 341))
        self.g_EvaluationGraph.setObjectName("g_EvaluationGraph")


        prediction = [14,17,8,9,14,9,12,17,13,19,18,23,17,30,31,41,39,34,51,52,45,51,66,61,71,77,80,70,126,96,73,73,94,107,83,70,77,54,70,68,55,38,47,32,38,26,34,23,24,18,13,14,13,7,13,15,10,10,18,16,12,10,16,20,21,17,21,27,28,18,36,58,99,63,105,60,57,114,110,92,94,104,97,87,78,74,95,121,79,84,82,65,78,52,35,36,33,36,33,16,30,10,19,19,10,11,10,21,10,10,13,8,8,12,12,13,15,23,36,40,33,51,43,70,51,65,56,65,95,93,97,92,131,122,162,121,102,77,92,63,104,100,78,77,70,67,48,38,37,27,30,21,19,18,13,14,14,14,12,14,12,9,15,14,11,10,19,19,30,19,22,32,34,39,36,41,49,56,57,65,83,97,137,122,106,99,77,97,73,110,86,81,64,77,59,66,88,49,49,49,45,34,25,25,21,24,22,14,7,17,16,12,14,11,10,19,16,13,15,30,17,26,29,35,24,41,43,52,45,75,74,102,88,126,105,125,85,81,126,98,115,99,91,95,66,76,60,50,52,53,34,43,28,32,21,22,24,14,20,16,14,11,9,10,7,11,17,11,14,13,13,10,12,25,20,19,22,29,28,50]
        actual = [9,3,6,11,7,7,15,9,6,6,6,7,10,8,7,12,3,2,7,5,5,7,7,7,7,10,13,10,14,11,20,25,17,18,25,21,31,32,26,35,28,37,41,34,30,39,39,39,34,30,37,29,26,15,22,15,20,14,10,21,14,14,9,11,5,6,7,11,4,3,2,6,10,7,5,3,12,13,10,13,13,8,21,18,8,7,20,14,14,7,14,10,13,27,13,18,16,16,20,17,4,15,8,6,12,15,11,10,15,17,7,7,8,9,12,12,5,4,11,4,5,7,1,1,4,2,6,3,4,10,12,21,26,21,30,45,56,75,83,82,126,119,137,131,112,82,73,43,55,55,53,46,43,29,22,26,13,17,8,13,10,17,19,9,9,9,3,7,7,0,2,3,3,1,3,3,3,7,3,5,11,5,5,6,6,4,4,8,14,12,16,10,16,18,15,23,17,33,15,13,11,14,17,19,20,12,21,7,19,10,13,10,8,21,11,9,14,14,15,18,16,12,20,8,3,13,4,1,10,8,13,10,21,18,21,34,25,34,33,40,42,36,72,75,76,92,71,112,106,101,170,135,106,68,48,48,26,33,29,17,12,13,17,15,14,15,10,9,2,6,8,5,1,2,3,4,3,1,3,5]
        error =[5,14,2,2,7,2,3,8,7,13,12,16,7,22,24,29,36,32,44,47,40,44,59,54,64,67,67,60,112,85,53,48,77,89,58,49,46,22,44,33,27,1,6,2,8,13,5,16,10,12,24,15,13,8,9,0,10,4,8,5,2,4,7,9,16,11,14,16,24,15,34,52,89,56,100,57,45,101,100,79,81,96,76,69,70,67,75,107,65,77,68,55,65,25,22,18,17,20,13,1,26,5,11,13,2,4,1,11,5,7,6,1,0,3,0,1,10,19,25,36,28,44,42,69,47,63,50,62,91,83,85,71,105,101,132,76,46,2,9,19,22,19,59,54,42,15,25,5,18,28,23,25,24,11,9,12,1,3,4,1,2,8,4,5,2,1,16,12,23,19,20,29,31,38,33,38,46,49,54,60,72,92,132,116,100,95,73,89,59,98,70,71,48,59,44,43,71,16,34,36,34,20,8,6,1,12,1,7,12,7,3,2,6,10,1,10,2,1,0,12,1,14,9,27,21,28,39,51,35,67,61,92,67,108,84,91,60,47,93,58,73,63,19,20,10,16,11,62,54,48,136,92,78,36,27,26,2,19,9,1,2,2,8,5,7,4,7,2,12,7,5,5,11,23,17,15,19,28,25,45]
        weekOfyear_x = []
        i = 1
        for x in prediction:
            weekOfyear_x.append(i)
            i = i + 1

        k = QtGui.QVBoxLayout()
        self.g_EvaluationGraph.setLayout(k)
        pc = pg.PlotWidget(name='Plot1')
        k.addWidget(pc)
        pc.setXRange(0, 200)
        pc.setYRange(0, 200)
        pred = pc.plot()
        pred.setPen((244, 66, 66))
        pred.setData(weekOfyear_x, prediction)

        act = pc.plot()
        act.setPen((116, 244, 65))
        act.setData(weekOfyear_x, actual)

        err = pc.plot()
        err.setPen((55, 229, 194))
        err.setData(weekOfyear_x, error)

        self.g_submissionGraphic = QtWidgets.QGraphicsView(self.Evaluation_tab)
        self.g_submissionGraphic.setGeometry(QtCore.QRect(0, 400, 31, 31))
        self.g_submissionGraphic.setObjectName("g_submissionGraphic")

        self.progressBar = QtWidgets.QProgressBar(self.Evaluation_tab)
        self.progressBar.setGeometry(QtCore.QRect(320, 340, 201, 31))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.lab_mae = QtWidgets.QLabel(self.Evaluation_tab)
        self.lab_mae.setGeometry(QtCore.QRect(40, 20, 31, 16))
        self.lab_mae.setObjectName("lab_mae")
        self.lab_mae.setText("MAE:")

        self.lab_gen_subFile = QtWidgets.QLabel(self.Evaluation_tab)
        self.lab_gen_subFile.setGeometry(QtCore.QRect(40, 400, 151, 30))
        self.lab_gen_subFile.setObjectName("lab_gen_subFile")
        self.lab_gen_subFile.setText( "Generate Submission File")

    def Setup_Analysis(self):

        self.l_ActionsList = QtWidgets.QListWidget(self.Analysis_tab)
        self.l_ActionsList.setGeometry(QtCore.QRect(10, 40, 256, 121))
        self.l_ActionsList.setObjectName("l_ActionsList")
        __sortingEnabled = self.l_ActionsList.isSortingEnabled()
        self.l_ActionsList.setSortingEnabled(False)
        self.l_ActionsList.setSortingEnabled(__sortingEnabled)

        item = QtWidgets.QListWidgetItem()
        self.l_ActionsList.addItem(item)
        item = self.l_ActionsList.item(0)
        item.setText("Graph Predictor")

        item = QtWidgets.QListWidgetItem()
        self.l_ActionsList.addItem(item)
        item = self.l_ActionsList.item(1)
        item.setText("Correlation")

        item = QtWidgets.QListWidgetItem()
        self.l_ActionsList.addItem(item)
        item = self.l_ActionsList.item(2)
        item.setText("Single Variable Regression")

        item = QtWidgets.QListWidgetItem()
        self.l_ActionsList.addItem(item)
        item = self.l_ActionsList.item(3)
        item.setText("Two Variable Plot")

        self.b_StartOver = QtWidgets.QPushButton(self.Analysis_tab)
        self.b_StartOver.setGeometry(QtCore.QRect(710, 400, 111, 32))
        self.b_StartOver.setObjectName("b_StartOver")
        self.b_StartOver.setText("Start Over")
        self.b_StartOver.clicked.connect(lambda: self.tabWidget.setCurrentWidget(self.Home_tab))

        self.lab_action = QtWidgets.QLabel(self.Analysis_tab)
        self.lab_action.setGeometry(QtCore.QRect(10, 20, 57, 16))
        self.lab_action.setObjectName("lab_action")
        self.lab_action.setText("Action")

        self.lab_xaxis = QtWidgets.QLabel(self.Analysis_tab)
        self.lab_xaxis.setGeometry(QtCore.QRect(10, 180, 41, 16))
        self.lab_xaxis.setObjectName("lab_xaxis")
        self.lab_xaxis.setText("x-axis:")

        self.cBox_xaxis = QtWidgets.QComboBox(self.Analysis_tab)
        self.cBox_xaxis.setGeometry(QtCore.QRect(50, 170, 231, 41))
        self.cBox_xaxis.setObjectName("cBox_xaxis")

        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.addItem("")
        self.cBox_xaxis.setItemText(19, "Outbreaks")
        self.cBox_xaxis.setItemText(0, "NDVI (NE)")
        self.cBox_xaxis.setItemText(1, "NDVI (NW)")
        self.cBox_xaxis.setItemText(2, "NDVI (SE)")
        self.cBox_xaxis.setItemText(3, "NDVI (SW)")
        self.cBox_xaxis.setItemText(4, "Precipitation (mm)")
        self.cBox_xaxis.setItemText(5, "Air Temperature (K)")
        self.cBox_xaxis.setItemText(6, "Average Air Temperature (K)")
        self.cBox_xaxis.setItemText(7, "Dew Point Temperature (K)")
        self.cBox_xaxis.setItemText(8, "Maximum Air Temperature (K)")
        self.cBox_xaxis.setItemText(9, "Minimum Air Temperature (K)")
        self.cBox_xaxis.setItemText(10, "Precipitation (kg/m^2)")
        self.cBox_xaxis.setItemText(11, "Relative Humidity (%)")
        # self.cBox_xaxis.setItemText(16, "Saturation Precipitation (mm)")
        self.cBox_xaxis.setItemText(12, "Specific Humidity (g/kg)")
        self.cBox_xaxis.setItemText(13, "TDTR (K)")
        self.cBox_xaxis.setItemText(14, "Station Average Temperature (C)")
        self.cBox_xaxis.setItemText(15, "Station DIUR Temperature Range (C)")
        self.cBox_xaxis.setItemText(16, "Station Maximum Temperature (C)")
        self.cBox_xaxis.setItemText(17, "Station Minimum Temperature (C)")
        self.cBox_xaxis.setItemText(18, "Station Precipitation (mm)")


        self.lab_yaxis = QtWidgets.QLabel(self.Analysis_tab)
        self.lab_yaxis.setGeometry(QtCore.QRect(10, 210, 41, 16))
        self.lab_yaxis.setObjectName("lab_yaxis")
        self.lab_yaxis.setText("y-axis:")

        self.cBox_yaxis = QtWidgets.QComboBox(self.Analysis_tab)
        self.cBox_yaxis.setGeometry(QtCore.QRect(50, 200, 231, 41))
        self.cBox_yaxis.setObjectName("cBox_yaxis")

        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.addItem("")
        self.cBox_yaxis.setItemText(19, "Outbreaks")
        self.cBox_yaxis.setItemText(0, "NDVI (NE)")
        self.cBox_yaxis.setItemText(1, "NDVI (NW)")
        self.cBox_yaxis.setItemText(2, "NDVI (SE)")
        self.cBox_yaxis.setItemText(3, "NDVI (SW)")
        self.cBox_yaxis.setItemText(4, "Precipitation (mm)")
        self.cBox_yaxis.setItemText(5, "Air Temperature (K)")
        self.cBox_yaxis.setItemText(6, "Average Air Temperature (K)")
        self.cBox_yaxis.setItemText(7, "Dew Point Temperature (K)")
        self.cBox_yaxis.setItemText(8, "Maximum Air Temperature (K)")
        self.cBox_yaxis.setItemText(9, "Minimum Air Temperature (K)")
        self.cBox_yaxis.setItemText(10, "Precipitation (kg/m^2)")
        self.cBox_yaxis.setItemText(11, "Relative Humidity (%)")
        #self.cBox_yaxis.setItemText(16, "Saturation Precipitation (mm)")
        self.cBox_yaxis.setItemText(12, "Specific Humidity (g/kg)")
        self.cBox_yaxis.setItemText(13, "TDTR (K)")
        self.cBox_yaxis.setItemText(14, "Station Average Temperature (C)")
        self.cBox_yaxis.setItemText(15, "Station DIUR Temperature Range (C)")
        self.cBox_yaxis.setItemText(16, "Station Maximum Temperature (C)")
        self.cBox_yaxis.setItemText(17, "Station Minimum Temperature (C)")
        self.cBox_yaxis.setItemText(18, "Station Precipitation (mm)")


        self.date_start = QtWidgets.QDateEdit(self.Analysis_tab)
        self.date_start.setGeometry(QtCore.QRect(80, 240, 110, 20))
        self.date_start.setObjectName("date_start")
        self.date_start.setEnabled(False)

        self.lab_startDate = QtWidgets.QLabel(self.Analysis_tab)
        self.lab_startDate.setGeometry(QtCore.QRect(10, 240, 71, 16))
        self.lab_startDate.setObjectName("lab_startDate")
        self.lab_startDate.setText("Start Date: ")

        self.lab_endData = QtWidgets.QLabel(self.Analysis_tab)
        self.lab_endData.setGeometry(QtCore.QRect(10, 270, 71, 16))
        self.lab_endData.setObjectName("lab_endData")
        self.lab_endData.setText("End Date: ")

        self.date_end = QtWidgets.QDateEdit(self.Analysis_tab)
        self.date_end.setGeometry(QtCore.QRect(80, 270, 110, 20))
        self.date_end.setObjectName("date_end")
        self.date_end.setEnabled(False)

        self.g_AnalysisGraph = QtWidgets.QGraphicsView(self.Analysis_tab)
        self.g_AnalysisGraph.setGeometry(QtCore.QRect(310, 20, 501, 341))
        self.g_AnalysisGraph.setObjectName("g_AnalysisGraph")

        self.l = QtGui.QVBoxLayout()
        self.g_AnalysisGraph.setLayout(self.l)
        self.pw = pg.GraphicsWindow(title="Analysis Plot")
        self.l.addWidget(self.pw)
        self.scatter = self.pw.addPlot(title="Analysis Plot")

        self.b_Graph = QtWidgets.QPushButton(self.Analysis_tab)
        self.b_Graph.setGeometry(QtCore.QRect(520, 370, 111, 32))
        self.b_Graph.setObjectName("b_Graph")
        self.b_Graph.setText("Graph")
        self.b_Graph.clicked.connect(lambda: graph(self))

    def openFile(self):
        return self.lab_fileLoc.setText(QFileDialog.getOpenFileName())

    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key_Enter:
    #         self.tabWidget.setCurrentWidget(self.DataSets_tab)


def selectAll(self):
    self.c_Precip_mm.setChecked(True)
    self.c_TDTR.setChecked(True)
    self.c_Air_Temp.setChecked(True)
    self.c_City.setChecked(True)
    self.c_Sta_Precip.setChecked(True)
    self.c_Sat_Precip.setChecked(True)
    self.c_Week_Of_Year.setChecked(True)
    self.c_NDVI_SW.setChecked(True)
    self.c_NDVI_NE.setChecked(True)
    self.c_Spec_Hum.setChecked(True)
    self.c_Sta_Avg_Temp.setChecked(True)
    self.c_Max_Air_Temp.setChecked(True)
    self.c_Rel_Hum.setChecked(True)
    self.c_NDVI_SE.setChecked(True)
    self.c_Sta_DUIR_Temp_Rang.setChecked(True)
    self.c_Year.setChecked(True)
    self.c_Dew_Point_Temp.setChecked(True)
    self.c_Week_Start_Date.setChecked(True)
    self.c_Precip_kg_per_m2.setChecked(True)
    self.c_Min_Air_Temp.setChecked(True)
    self.c_Sta_Max_Temp.setChecked(True)
    self.c_Sta_Min_Temp.setChecked(True)
    self.c_NDVI_NW.setChecked(True)

def deselectAll(self):
    self.c_Precip_mm.setChecked(False)
    self.c_TDTR.setChecked(False)
    self.c_Air_Temp.setChecked(False)
    self.c_City.setChecked(False)
    self.c_Sta_Precip.setChecked(False)
    self.c_Sat_Precip.setChecked(False)
    self.c_Week_Of_Year.setChecked(False)
    self.c_NDVI_SW.setChecked(False)
    self.c_NDVI_NE.setChecked(False)
    self.c_Spec_Hum.setChecked(False)
    self.c_Sta_Avg_Temp.setChecked(False)
    self.c_Max_Air_Temp.setChecked(False)
    self.c_Rel_Hum.setChecked(False)
    self.c_NDVI_SE.setChecked(False)
    self.c_Sta_DUIR_Temp_Rang.setChecked(False)
    self.c_Year.setChecked(False)
    self.c_Dew_Point_Temp.setChecked(False)
    self.c_Week_Start_Date.setChecked(False)
    self.c_Precip_kg_per_m2.setChecked(False)
    self.c_Min_Air_Temp.setChecked(False)
    self.c_Sta_Max_Temp.setChecked(False)
    self.c_Sta_Min_Temp.setChecked(False)
    self.c_NDVI_NW.setChecked(False)

def graph(self):
    self.scatter.clear()
    data = input_parser('sj')
    xGrab = str(self.cBox_xaxis.currentText())
    xIndex = int(str(self.cBox_xaxis.currentIndex()))
    yGrab = str(self.cBox_yaxis.currentText())
    yIndex = int(str(self.cBox_yaxis.currentIndex()))
    listOfPredictors = list(data.training_features)
    outbreaksData = data.training_labels['total_cases'].values
    outbreakLabel = "Cases"
    action = []
    x = []
    y = []

    try:
        action = self.l_ActionsList.selectedIndexes()[0]
    except:
        pass

    self.b_Graph.setEnabled(False)

    if action.data() == 'Graph Predictor':
        if xIndex < 18:
            indexX_name = str(listOfPredictors[xIndex])
            x = data.training_features[indexX_name].values
        else:
            x = data.training_labels['total_cases'].values
            xGrab = outbreakLabel

        y = data.training_labels['total_cases'].values

        self.scatter.setLabel('left', 'Cases')
        self.scatter.setLabel('bottom', xGrab)

    elif action.data() == 'Correlation':
        x = [5, 4, 3, 2, 1]
        y = [1, 2, 3, 4, 5]
        self.scatter.plot(x, y, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(50, 100, 255, 50))
        x = [7, 9, 11, 22, 13]
        y = [5, 22, 13, 24, 35]
        self.scatter.plot(x, y, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(50, 100, 255, 50))

        self.scatter.setLabel('left', yGrab)
        self.scatter.setLabel('bottom', xGrab)

    elif action.data() == 'Single Variable Regression':

        if xIndex < 18:
            indexX_name = str(listOfPredictors[xIndex])
            x = data.training_features[indexX_name].values
        else:
            x = data.training_labels['total_cases'].values
            xGrab = outbreakLabel
        if xIndex < 18:
            indexY_name = str(listOfPredictors[yIndex])
            y = data.training_features[indexY_name].values
        else:
            y = data.training_labels['total_cases'].values
            yGrab = outbreakLabel

        self.scatter.setLabel('left', yGrab)
        self.scatter.setLabel('bottom', xGrab)

        axes = plt.gca()
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        x_vals = np.array(axes.get_xlim())
        y_vals = intercept + slope * x_vals

        self.scatter.plot(x_vals, y_vals, pen=(0,128,0), symbol=None, symbolPen='w', symbolSize=10, symbolBrush=(50, 100, 255, 50))


    elif action.data() == 'Two Variable Plot':
        if xIndex < 18:
            indexX_name = str(listOfPredictors[xIndex])
            x = data.training_features[indexX_name].values
        else:
            x = data.training_labels['total_cases'].values
            xGrab = outbreakLabel
        if xIndex < 18:
            indexY_name = str(listOfPredictors[yIndex])
            y = data.training_features[indexY_name].values
        else:
            y = data.training_labels['total_cases'].values
            yGrab = outbreakLabel

        self.scatter.setLabel('left', yGrab)
        self.scatter.setLabel('bottom', xGrab)

    else:
        self.msgBox = QMessageBox()
        self.msgBox.setText("Error")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.show()

    self.scatter.plot(x, y, pen=None, symbol='o', symbolPen=None, symbolSize=10, symbolBrush=(50, 100, 255, 50))
    self.b_Graph.setEnabled(True)

def input_parser(city_name):
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

    return City(city_name, training_features[training_features['city'] == city_name].drop(['city'], axis=1),
                training_labels[training_labels['city'] == city_name].drop(['city'], axis=1),
                test_features[test_features['city'] == city_name].drop(['city'], axis=1),
                submission[submission['city'] == city_name].drop(['city'], axis=1))


# I dont think this should change
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()

