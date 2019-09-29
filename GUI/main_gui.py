# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DengueAI.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DengAI(object):
    def setupUi(self, DengAI):
        DengAI.setObjectName("DengAI")
        DengAI.resize(850, 525)
        self.centralWidget = QtWidgets.QWidget(DengAI)
        self.centralWidget.setObjectName("centralWidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 831, 461))
        self.tabWidget.setObjectName("tabWidget")

        self.Home_tab = QtWidgets.QWidget()
        self.Home_tab.setObjectName("Home_tab")
        self.tabWidget.addTab(self.Home_tab, "")

        self.DataSets_tab = QtWidgets.QWidget()
        self.DataSets_tab.setObjectName("DataSets_tab")
        self.tabWidget.addTab(self.DataSets_tab, "")
        self.DataSets_tab.setEnabled(False)

        self.Predictors_tab = QtWidgets.QWidget()
        self.Predictors_tab.setObjectName("Predictors_tab")
        self.tabWidget.addTab(self.Predictors_tab, "")
        self.Predictors_tab.setEnabled(False)

        self.Algorithm_tab = QtWidgets.QWidget()
        self.Algorithm_tab.setObjectName("Algorithm_tab")
        self.tabWidget.addTab(self.Algorithm_tab, "")
        self.Algorithm_tab.setEnabled(False)

        self.Evaluation_tab = QtWidgets.QWidget()
        self.Evaluation_tab.setObjectName("Evaluation_tab")
        self.tabWidget.addTab(self.Evaluation_tab, "")

        self.Analysis_tab = QtWidgets.QWidget()
        self.Analysis_tab.setObjectName("Analysis_tab")
        self.tabWidget.addTab(self.Analysis_tab, "")

        DengAI.setCentralWidget(self.centralWidget)

        self.statusBar = QtWidgets.QStatusBar(DengAI)
        self.statusBar.setObjectName("statusBar")
        DengAI.setStatusBar(self.statusBar)

        self.retranslateUi(DengAI)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DengAI)

    def retranslateUi(self, DengAI):
        _translate = QtCore.QCoreApplication.translate
        DengAI.setWindowTitle(_translate("DengAI", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Home_tab), _translate("DengAI", "Home"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DataSets_tab), _translate("DengAI", "Data Sets"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Predictors_tab), _translate("DengAI", "Predictors"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Algorithm_tab), _translate("DengAI", "Algorithm"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Evaluation_tab), _translate("DengAI", "Evaluation"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Analysis_tab), _translate("DengAI", "Analysis"))


