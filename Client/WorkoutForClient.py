import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime as dt, datetime
import Controller

class WorkoutForClient(QWidget):
    def __init__(self, id, trainerID):
        self.width = 1000
        self.height = 500
        super().__init__()

        self.backButtonName = "Назад"

        self.countExerciseCurrentWorkout = 1
        self.countExercise = 1
        self.countSet = 1

        self.ID = id
        self.trainerID = trainerID
        self.time = None
        self.controller = Controller.Controller()
        self.exerciseItems = self.controller.getExerciseNames()
        self.list = self.controller.getWOD(self.ID)
        self.initUi()

    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Тренировка')
        self.createWorkout()

    def createWorkout(self):

############# WOD space
        self.wodBox = QVBoxLayout()
        wodGroup = QGroupBox()
        wodGroup.setLayout(self.wodBox)
        if self.list == []:
            pass
        else:
            count = 1
            time = None
            for t in self.list:
                if (t[0] != time):
                    time = t[0]
                    self.addWodButton(time, count)
                    count += 1


############# Workout space

        self.scrollCurrentWorkout = QScrollArea()
        self.scrollCurrentWorkout.setWidgetResizable(True)
        self.scrollContent = QWidget(self.scrollCurrentWorkout)
        self.scrollCurrentWorkoutLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollCurrentWorkoutLayout)
        self.scrollCurrentWorkout.setWidget(self.scrollContent)



############# Planned workout space

        self.scrollPlannedWorkout = QScrollArea()
        self.scrollPlannedWorkout.setWidgetResizable(True)
        self.scrollContentPlannedWorkout = QWidget(self.scrollPlannedWorkout)
        self.scrollPlannedWorkoutLayout = QVBoxLayout(self.scrollContentPlannedWorkout)
        self.scrollContentPlannedWorkout.setLayout(self.scrollPlannedWorkoutLayout)
        self.scrollPlannedWorkout.setWidget(self.scrollContentPlannedWorkout)

        self.plannedWorkoutLabel = QLabel('Запланированная тренировка', self)
        self.scrollPlannedWorkoutLayout.addWidget(self.plannedWorkoutLabel)


############# Buttons space

        buttonBox = QVBoxLayout()
        buttonGroup = QGroupBox()
        addExerciseButton = QPushButton('Добавить упражнение', self)
        addExerciseButton.clicked.connect(self.addExerciseFunc)
        removeExerciseButton = QPushButton('Удалить упражнение', self)
        removeExerciseButton.clicked.connect(self.removeExercise)
        addWorkoutButton = QPushButton("Добавить тренировку", self)
        addWorkoutButton.clicked.connect(self.addWorkoutFunc)

        buttonBox.addWidget(addExerciseButton)
        buttonBox.addWidget(removeExerciseButton)
        buttonBox.addWidget(addWorkoutButton)
        buttonGroup.setLayout(buttonBox)


        self.quitButton = QPushButton(self.backButtonName, self)
        self.quitButton.clicked.connect(self.close)


        # Window layout
        self.grid = QGridLayout()
        self.grid.setSpacing(10)


        self.grid.addWidget(wodGroup, 0, 0)
        self.grid.addWidget(self.scrollPlannedWorkout, 0, 2)
        self.grid.addWidget(self.scrollCurrentWorkout, 0, 3)
        self.grid.addWidget(buttonGroup, 1, 3)
        self.grid.addWidget(self.quitButton, 2, 0)


        self.setLayout(self.grid)



    def addWorkoutFunc(self):
        if self.list == []:
            self.controller.insertWorkoutClientWithoutTime(self.ID, self.trainerID)
        else:
            self.controller.insertWorkoutClient(self.time, self.ID, self.trainerID)
        if self.scrollCurrentWorkoutLayout is not None:
            for i in range(self.scrollCurrentWorkoutLayout.count()):
                print(self.scrollCurrentWorkoutLayout.count())
                layout1 = self.scrollCurrentWorkoutLayout.itemAt(i)
                for j in range(layout1.count()-1):
                    print(layout1.count())
                    item = layout1.itemAt(j+1)
                    widget = item.widget()
                    if widget is not None:
                        try:
                            valueComboBox = widget.text()
                            self.controller.insertExercise(valueComboBox)
                        except AttributeError:
                            valueComboBox = widget.currentText()
                            self.controller.insertExercise(valueComboBox)
                    else:
                        layout2 = item.layout()
                        weight = layout2.itemAt(0).widget().text()
                        reps = layout2.itemAt(1).widget().text()
                        if weight == '+':
                            pass
                        else:
                            self.controller.insertSet(weight, reps)
        self.close()


    def showCurrentWorkout(self, time):
        self.countExerciseCurrentWorkout = 1
        self.countInLayout = self.scrollCurrentWorkoutLayout.count()
        exercise = ''
        if self.list == []:
            pass
        else:
            for i in range(self.scrollCurrentWorkoutLayout.count()):
                self.removeWorkout()
                self.countInLayout -= 1
            for elem in self.list:
                if elem[0] == time:
                    if elem[1] == exercise:
                        self.addSetCurrentWorkout(self.scrollCurrentWorkoutLayout.itemAt(self.scrollCurrentWorkoutLayout.count()-1), elem[2])
                    else:
                        self.addExerciseCurrentWorkout(elem[1], elem[2])
                        exercise = elem[1]
                        self.countExerciseCurrentWorkout += 1


    def addSetCurrentWorkout(self, layout, weight):
        setBox = QHBoxLayout()
        weightEdit = QLineEdit(str(weight))
        repsEdit = QLineEdit()
        repsEdit.setPlaceholderText("Повторения ...")
        setBox.addWidget(weightEdit)
        setBox.addWidget(repsEdit)
        layout.addLayout(setBox)


    def addExerciseCurrentWorkout(self, name, weight):
        workoutBox = QVBoxLayout()
        exerciseNumLabel = QLabel("Упражнение " + str(self.countExerciseCurrentWorkout))
        exerciseNameLabel = QLabel(name)

        setBox = QHBoxLayout()
        weightEdit = QLineEdit(str(weight))
        repsEdit = QLineEdit()
        repsEdit.setPlaceholderText("Повторения ...")

        workoutBox.addWidget(exerciseNumLabel)
        workoutBox.addWidget(exerciseNameLabel)
        setBox.addWidget(weightEdit)
        setBox.addWidget(repsEdit)
        workoutBox.addLayout(setBox)
        self.scrollCurrentWorkoutLayout.addLayout(workoutBox)



    def addWodButton(self, time, count):
        strWodButtons = ''
        strWodButtons += str(count) + ") " + str(time)
        wodButton = QPushButton(strWodButtons)
        wodButton.clicked.connect(lambda: {self.showWOD(time), self.showCurrentWorkout(time)})
        self.wodBox.addWidget(wodButton)

    def showWOD(self, time):
        self.time = time
        self.countExercise = 1
        countSet = 1
        exercise = ''
        strWorkout = "Тренировка ({0})\n".format(time)
        if self.list == []:
            self.plannedWorkoutLabel.setText("Сегодня тренировок нет")
        else:
            for elem in self.list:
                if elem[0] == time:
                    if elem[1] == exercise:
                        countSet += 1
                        strWorkout += "\t" + str(countSet) + ") Вес: " + str(elem[2]) + " Повторения: " + str(elem[3]) + "\n"
                    else:
                        exercise = elem[1]
                        strWorkout += str(self.countExercise) + ". " + exercise + "\n"
                        self.countExercise += 1
                        countSet = 1
                        strWorkout += "\t" + str(countSet) + ") Вес: " + str(elem[2]) + " Повторения: " + str(elem[3]) + "\n"

            self.plannedWorkoutLabel.setText(strWorkout)






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

        workoutBox = QVBoxLayout()
        buttonBox = QHBoxLayout()
        exerciseBox = QComboBox()
        exerciseBox.addItems(self.exerciseItems)
        exerciseLabel = QLabel("Упражнение " + str(self.countExerciseCurrentWorkout))
        self.countExerciseCurrentWorkout += 1

        addSetButton = QPushButton('+')
        addSetButton.pressed.connect(lambda: self.addSetFunc(workoutBox))
        removeSetButton = QPushButton('-')
        removeSetButton.clicked.connect(lambda: self.removeSetFunc(workoutBox))


        workoutBox.addWidget(exerciseLabel)
        workoutBox.addWidget(exerciseBox)
        buttonBox.addWidget(addSetButton)
        buttonBox.addWidget(removeSetButton)
        workoutBox.addLayout(buttonBox)
        self.scrollCurrentWorkoutLayout.addLayout(workoutBox)



    def removeExercise(self):
        self.countExerciseCurrentWorkout -= 1
        countInLayout = self.scrollCurrentWorkoutLayout.count()
        layout1 = self.scrollCurrentWorkoutLayout.itemAt(countInLayout - 1)
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

    def removeWorkout(self):
        layout1 = self.scrollCurrentWorkoutLayout.itemAt(self.countInLayout - 1)
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