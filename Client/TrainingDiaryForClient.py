import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import Controller
from Client import CalendarForClient
from Client import ChangeTrainer
from Client import WorkoutForClient


class TrainingDiaryForClient(QWidget):
    def __init__(self, id):
        self.width = 800
        self.height = 500
        super().__init__()

        self.ID = id

        self.backButtonName = "Назад"

        self.controller = Controller.Controller()
        self.trainerID = self.controller.getTrainerID(self.ID)
        self.initUi()


    def createWindow(self):

        createWorkoutButton = QPushButton("Тренировки")
        createWorkoutButton.clicked.connect(self.goWorkoutFunc)

        goCalendarButton = QPushButton("Журнал")
        goCalendarButton.clicked.connect(self.goCalendarFunc)

        goChangeButton = QPushButton("Поменять тренера ")
        goChangeButton.clicked.connect(self.goChangeTrainer)


        vbox = QVBoxLayout()
        vbox.addWidget(createWorkoutButton)
        vbox.addWidget(goCalendarButton)
        vbox.addWidget(goChangeButton)

        self.setLayout(vbox)

    def goWorkoutFunc(self):
        self.workout = WorkoutForClient.WorkoutForClient(self.ID, self.trainerID)
        self.workout.show()

    def goCalendarFunc(self):
        self.calendar = CalendarForClient.CalendarForClient(self.ID, self.trainerID)
        self.calendar.show()

    def goChangeTrainer(self):
        self.changeWindow = ChangeTrainer.ChangeTrainer(self.ID)
        self.changeWindow.show()


    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Дневник')

        self.createWindow()



    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
