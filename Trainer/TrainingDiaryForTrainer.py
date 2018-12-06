from PyQt5.QtWidgets import *

import Controller
from Trainer import WorkoutForTrainer


class TrainingDiaryForTrainer(QWidget):
    def __init__(self, id):
        self.width = 800
        self.height = 500
        super().__init__()

        self.id = id

        self.backButtonName = "Назад"

        self.controller = Controller.Controller()

        self.initUi()


    def createWindow(self):

        createWorkoutButton = QPushButton("Тренировки")
        createWorkoutButton.clicked.connect(self.goCreateWorkoutFunc)


        vbox = QVBoxLayout(self)
        vbox.addWidget(createWorkoutButton)

        self.setLayout(vbox)

    def goCreateWorkoutFunc(self):
        self.workout = WorkoutForTrainer.WorkoutForTrainer(self.id)
        self.workout.show()

    def goCalendarFunc(self):
        # self.calendar = CalendarForClient.Calendar()
        # self.calendar.show()
        pass


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
