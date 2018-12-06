import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import Controller

class CalendarForClient(QWidget):
    def __init__(self, id, trainerID):
        self.width = 1000
        self.height = 500
        super().__init__()

        self.backButtonName = "Назад"

        self.ID = id
        self.trainerID = trainerID
        self.time = None
        self.controller = Controller.Controller()
        self.listPlanned = None
        self.listDone = None


        self.count = 1
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Журнал')
        self.createCalendar()

    def createCalendar(self):

        hbox1 = QHBoxLayout()
        group1 = QGroupBox()
        calendar = QCalendarWidget()
        calendar.setGridVisible(True)
        calendar.setFixedSize(250, 300)
        calendar.clicked[QDate].connect(self.selectDateAndWorkout)
        hbox1.addWidget(calendar)
        group1.setLayout(hbox1)


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



        self.quitButton = QPushButton(self.backButtonName, self)
        self.quitButton.clicked.connect(self.close)
        self.quitButton.resize(self.quitButton.sizeHint())



        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(group1, 0, 1)
        grid.addWidget(self.scrollPlannedWorkout, 0, 2)
        grid.addWidget(self.scrollDoneWorkout, 0, 3)


        grid.addWidget(self.quitButton, 1, 0)



        self.setLayout(grid)

    def showWorkout(self, list, label):
        countExercise = 1
        if list == []:
            label.setText('Не было тренировки')
        else:
            strPlannedWorkout = ''
            exercise = ''
            time = None
            for elem in list:
                if elem[0] != time:
                    exercise = ''
                    time = elem[0]
                    countExercise = 1
                    strPlannedWorkout += "\n"
                    strPlannedWorkout += "Тренировка (" + str(time) + ")\n"
                    if elem[1] != exercise:
                        exercise = elem[1]
                        strPlannedWorkout += "\t" + str(countExercise) + ") " + exercise + ":"
                        strPlannedWorkout += "\n\t\t" + "Вес: " + str(elem[2]) + " Повторения: " + str(elem[3]) + "\n"
                        countExercise += 1
                    else:
                        strPlannedWorkout += "\t\t" + "Вес: " + str(elem[2]) + " Повторения: " + str(elem[3]) + "\n"
                else:
                    if elem[1] != exercise:
                        exercise = elem[1]
                        strPlannedWorkout += "\t" + str(countExercise) + ") " + exercise + ":"
                        strPlannedWorkout += "\n\t\t" + "Вес: " + str(elem[2]) + " Повторения: " + str(elem[3]) + "\n"
                        countExercise += 1
                    else:
                        strPlannedWorkout += "\t\t" + "Вес: " + str(elem[2]) + " Повторения: " + str(elem[3]) + "\n"

            label.setText(strPlannedWorkout)


    def selectDateAndWorkout(self, date):
        self.listPlanned = self.controller.getPlannedWorkout(date.toPyDate(), self.ID)
        self.listDone = self.controller.getDoneWorkout(date.toPyDate(), self.ID)

        self.showWorkout(self.listPlanned, self.plannedWorkoutLabel)
        self.showWorkout(self.listDone, self.doneWorkoutLabel)




    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())