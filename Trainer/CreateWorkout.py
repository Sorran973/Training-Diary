import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime

from dateutil.parser import parser

import Controller

class CreateWorkout(QWidget):
    def __init__(self, id, clientID):
        self.width = 1000
        self.height = 500
        super().__init__()

        self.backButtonName = "Назад"

        self.countExercise = 0
        self.countSet = 1

        self.ID = id
        self.clientID = clientID
        self.controller = Controller.Controller()
        self.exerciseItems = self.controller.getExerciseNames()

        self.initUi()

    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Создание тренировки')
        self.createWorkout()

    def createWorkout(self):

        dateAndTimeBox = QVBoxLayout()
        dateAndTimeGroup = QGroupBox()
        self.dateLine = QLineEdit()
        self.dateLine.setPlaceholderText("Дата ...")
        self.timeLine = QLineEdit()
        self.timeLine.setPlaceholderText("Время ...")


        self.addExerciseButton = QPushButton('Добавить упражнение', self)
        self.addExerciseButton.clicked.connect(self.addExerciseFunc)
        self.removeExerciseButton = QPushButton('Удалить упражнение', self)
        self.removeExerciseButton.clicked.connect(self.removeExercise)
        self.createWorkoutButton = QPushButton("Создать тренировку", self)
        self.createWorkoutButton.clicked.connect(self.createWorkoutFunc)

        dateAndTimeBox.addWidget(self.dateLine)
        dateAndTimeBox.addWidget(self.timeLine)
        dateAndTimeBox.addWidget(self.addExerciseButton)
        dateAndTimeBox.addWidget(self.removeExerciseButton)
        dateAndTimeBox.addWidget(self.createWorkoutButton)
        dateAndTimeGroup.setLayout(dateAndTimeBox)


        self.scrollNewWorkout = QScrollArea()
        self.scrollNewWorkout.setWidgetResizable(True)
        self.scrollContent = QWidget(self.scrollNewWorkout)
        self.scrollNewWorkoutLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollNewWorkoutLayout)
        self.scrollNewWorkout.setWidget(self.scrollContent)

        self.quitButton = QPushButton(self.backButtonName, self)
        self.quitButton.clicked.connect(self.close)


########### Window layout

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(dateAndTimeGroup, 0, 1)
        self.grid.addWidget(self.scrollNewWorkout, 0, 2)
        self.grid.addWidget(self.quitButton, 2, 0)

        self.setLayout(self.grid)



    def createWorkoutFunc(self):
        date = QtCore.QDate.fromString(self.dateLine.text(), 'dd.MM.yyyy')
        time = QtCore.QTime.fromString(self.timeLine.text(), 'hh:mm:ss')
        print(time)
        print(time.toPyTime())

        self.controller.insertWorkoutFromTrainer(date.toPyDate(), time.toPyTime(), self.ID, self.clientID)
        if self.scrollNewWorkoutLayout is not None:
            for i in range(self.scrollNewWorkoutLayout.count()):
                layout1 = self.scrollNewWorkoutLayout.itemAt(i)
                for j in range(layout1.count()-1):
                    item = layout1.itemAt(j+1)
                    widget = item.widget()
                    if widget is not None:
                        valueComboBox = widget.currentText()
                        self.controller.insertExercise(valueComboBox)
                    else:
                        layout2 = item.layout()
                        weight = layout2.itemAt(0).widget().text()
                        if weight == '+':
                            pass
                        else:
                            reps = layout2.itemAt(1).widget().text()
                            self.controller.insertSet(weight, reps)
        self.close()


    def addSetFunc(self, layout):
        setBox = QHBoxLayout()
        weightEdit = QLineEdit()
        weightEdit.setPlaceholderText("Вес ...")
        repsEdit = QLineEdit()
        repsEdit.setPlaceholderText("Повторения ...")
        setBox.addWidget(weightEdit)
        setBox.addWidget(repsEdit)
        layout.addLayout(setBox)


    def removeSetFunc(self, layout):
        countInLayout = layout.count()
        layout1 = layout.itemAt(countInLayout-1)
        if layout1 is not None:
            while layout1.count():
                item = layout1.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            layout1.deleteLater()


    def addExerciseFunc(self):
        self.countExercise += 1

        workoutBox = QVBoxLayout()
        buttonBox = QHBoxLayout()
        exerciseBox = QComboBox()
        exerciseBox.addItems(self.exerciseItems)
        exerciseLabel = QLabel("Упражнение " + str(self.countExercise))

        addSetButton = QPushButton('+')
        addSetButton.pressed.connect(lambda: self.addSetFunc(workoutBox))
        removeSetButton = QPushButton('-')
        removeSetButton.clicked.connect(lambda: self.removeSetFunc(workoutBox))


        workoutBox.addWidget(exerciseLabel)
        workoutBox.addWidget(exerciseBox)
        buttonBox.addWidget(addSetButton)
        buttonBox.addWidget(removeSetButton)
        workoutBox.addLayout(buttonBox)
        self.scrollNewWorkoutLayout.addLayout(workoutBox)


    def removeExercise(self):
        self.countExercise -= 1
        countInLayout = self.scrollNewWorkoutLayout.count()
        layout1 = self.scrollNewWorkoutLayout.itemAt(countInLayout - 1)
        if layout1 is not None:
            while layout1.count():
                item = layout1.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    layout2 = item.layout()
                    while layout2.count():
                        item1 = layout2.takeAt(0)
                        widget1 = item1.widget()
                        if widget1 is not None:
                            widget1.deleteLater()
                    layout2.deleteLater()
            layout1.deleteLater()


    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())