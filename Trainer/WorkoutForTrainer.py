import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime

from dateutil.parser import parser

import Controller
from Trainer import CreateWorkout

class WorkoutForTrainer(QWidget):
    def __init__(self, id):
        self.width = 1200
        self.height = 500
        super().__init__()

        self.backButtonName = "Назад"

        self.countExercixe = 0
        self.countSet = 1

        self.ID = id
        self.controller = Controller.Controller()
        self.clientNames = self.controller.getClientNames(self.ID)
        self.clientID = None

        self.initUi()

    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Создание тренировки')
        self.createWorkout()

    def createWorkout(self):


########### Name and Date space

        clientNameAndDateVBox = QVBoxLayout()
        clientNameAndDateGroup = QGroupBox()
        self.clientNamesBox = QComboBox()
        self.clientNamesBox.addItems(self.clientNames)
        self.clientID = self.clientNamesBox.currentText().split()[-1]
        clientNameAndDateVBox.addWidget(self.clientNamesBox)

        intervalHBox = QHBoxLayout()
        self.fromDateLine = QLineEdit()
        self.fromDateLine.setPlaceholderText("С ...")
        self.toDateLine = QLineEdit()
        self.toDateLine.setPlaceholderText("До ...")
        self.showDateButton = QPushButton("Показать")
        self.showDateButton.clicked.connect(self.showDate)
        intervalHBox.addWidget(self.fromDateLine)
        intervalHBox.addWidget(self.toDateLine)
        intervalHBox.addWidget(self.showDateButton)
        clientNameAndDateVBox.addLayout(intervalHBox)
        clientNameAndDateGroup.setLayout(clientNameAndDateVBox)


        self.scrollDateInInterval = QScrollArea()
        self.scrollDateInInterval.setWidgetResizable(True)
        self.scrollContent = QWidget(self.scrollDateInInterval)
        self.scrollDateInIntervalLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollDateInIntervalLayout)
        self.scrollDateInInterval.setWidget(self.scrollContent)

        self.dateLabel = QLabel("Все тренировки с клиентом")
        self.scrollDateInIntervalLayout.addWidget(self.dateLabel)


############# PlannedWorkout space

        self.scrollPlannedWorkout = QScrollArea()
        self.scrollPlannedWorkout.setWidgetResizable(True)
        self.scrollContentPlannedWorkout = QWidget(self.scrollPlannedWorkout)
        self.scrollPlannedWorkoutLayout = QVBoxLayout(self.scrollContentPlannedWorkout)
        self.scrollContentPlannedWorkout.setLayout(self.scrollPlannedWorkoutLayout)
        self.scrollPlannedWorkout.setWidget(self.scrollContentPlannedWorkout)

        self.plannedWorkoutLabel = QLabel('Запланированная тренировка')
        self.scrollPlannedWorkoutLayout.addWidget(self.plannedWorkoutLabel)


############# DoneWorkout space

        self.scrollDoneWorkout = QScrollArea()
        self.scrollDoneWorkout.setWidgetResizable(True)
        self.scrollContentDoneWorkout = QWidget(self.scrollDoneWorkout)
        self.scrollDoneWorkoutLayout = QVBoxLayout(self.scrollContentDoneWorkout)
        self.scrollContentDoneWorkout.setLayout(self.scrollDoneWorkoutLayout)
        self.scrollDoneWorkout.setWidget(self.scrollContentDoneWorkout)

        self.doneWorkoutLabel = QLabel('Выполненная тренировка')
        self.scrollDoneWorkoutLayout.addWidget(self.doneWorkoutLabel)


############ CreateWorkoutButton space

        createWorkoutBox = QVBoxLayout()
        createWorkoutBoxGroup = QGroupBox()
        createWorkoutButton = QPushButton("Добавить тренировку", self)
        createWorkoutButton.clicked.connect(self.createWorkoutFunc)
        createWorkoutBox.addWidget(createWorkoutButton)
        createWorkoutBoxGroup.setLayout(createWorkoutBox)


        self.quitButton = QPushButton(self.backButtonName, self)
        self.quitButton.clicked.connect(self.close)
        self.quitButton.resize(self.quitButton.sizeHint())


        # Window layout
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(clientNameAndDateGroup, 0, 1)
        self.grid.addWidget(self.scrollDateInInterval, 1, 1)
        self.grid.addWidget(createWorkoutBoxGroup, 0, 4)
        self.grid.addWidget(self.scrollPlannedWorkout, 1, 3)
        self.grid.addWidget(self.scrollDoneWorkout, 1, 4)
        self.grid.addWidget(self.quitButton, 2, 0)


        self.setLayout(self.grid)




    def createWorkoutFunc(self):
        self.createNewWorkout = CreateWorkout.CreateWorkout(self.ID, self.clientID)
        self.createNewWorkout.show()


    def showDate(self):
        n = self.scrollDateInIntervalLayout.count()-1
        for i in range(self.scrollDateInIntervalLayout.count()-1):
            self.scrollDateInIntervalLayout.takeAt(n).widget().deleteLater()
            n -= 1
        self.clientID = self.clientNamesBox.currentText().split()[-1]
        fromDate = QtCore.QDate.fromString(self.fromDateLine.text(), 'dd.MM.yyyy')
        toDate = QtCore.QDate.fromString(self.toDateLine.text(), 'dd.MM.yyyy')

        dateList = self.controller.getWorkoutsInInterval(self.clientID, fromDate.toPyDate(), toDate.toPyDate())
        if dateList == []:
            self.dateLabel.setText("Тренировок нет")
        else:
            for elem in dateList:
                self.createDateButton(elem[0], elem[1])

    def createDateButton(self, date, time):
        strWodButtons = ''
        strWodButtons += str(date) + " " + str(time)
        showWorkoutButton = QPushButton(strWodButtons)
        showWorkoutButton.clicked.connect(lambda: {self.showPlannedWorkout(date, time), self.showDoneWorkout(date, time)})
        self.scrollDateInIntervalLayout.addWidget(showWorkoutButton)


    def showPlannedWorkout(self, date, time):
        list = self.controller.getPlannedWorkoutTrainer(date, time, self.clientID)
        self.count = 1
        strWorkout = "Тренировка ({0} {1})\n".format(date, time)
        if list == []:
            self.plannedWorkoutLabel.setText("Тренировок нет")
        else:
            exercise = ''
            for e in list:
                if (e[0] != exercise):
                    exercise = e[0]
                    strWorkout += str(self.count) + ". " + exercise + "\n"
                    strWorkout += "\t" + "Вес: " + str(e[1]) + " Повторений: " + str(e[2]) + "\n"
                    self.count += 1
                else:
                    strWorkout += "\t" + "Вес: " + str(e[1]) + " Повторений: " + str(e[2]) + "\n"
            self.plannedWorkoutLabel.setText(strWorkout)


    def showDoneWorkout(self, date, time):
        list = self.controller.getDoneWorkoutTrainer(date, time, self.clientID)
        self.count = 1
        strWorkout = "Тренировка ({0} {1})\n".format(date, time)
        if list == []:
            self.doneWorkoutLabel.setText("Тренировок нет")
        else:
            exercise = ''
            for e in list:
                if (e[0] != exercise):
                    exercise = e[0]
                    strWorkout += str(self.count) + ". " + exercise + "\n"
                    strWorkout += "\t" + "Вес: " + str(e[1]) + " Повторений: " + str(e[2]) + "\n"
                    self.count += 1
                else:
                    strWorkout += "\t" + "Вес: " + str(e[1]) + " Повторений: " + str(e[2]) + "\n"
            self.doneWorkoutLabel.setText(strWorkout)


    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())