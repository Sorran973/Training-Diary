import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime

from dateutil.parser import parser

import Controller

class ChangeTrainer(QWidget):
    def __init__(self, id):
        self.width = 800
        self.height = 500
        super().__init__()

        self.backButtonName = "Назад"

        self.ID = id
        self.controller = Controller.Controller()

        self.initUi()

    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Смена тренера')
        self.createWorkout()

    def createWorkout(self):

        dateAndTimeBox = QVBoxLayout()
        dateAndTimeGroup = QGroupBox()
        self.line = QLineEdit()
        self.line.setPlaceholderText("Введите id тренера ...")



        self.changeButton = QPushButton('Сменить', self)
        self.changeButton.clicked.connect(self.changeFunc)


        dateAndTimeBox.addWidget(self.line)
        dateAndTimeBox.addWidget(self.changeButton)
        dateAndTimeGroup.setLayout(dateAndTimeBox)

        self.quitButton = QPushButton(self.backButtonName, self)
        self.quitButton.clicked.connect(self.close)

########### Window layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(dateAndTimeGroup, 0, 1)
        self.grid.addWidget(self.quitButton, 1, 0)

        self.setLayout(self.grid)



    def changeFunc(self):
        self.controller.changeTrainer(self.ID, self.line.text())
        self.close()


    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())