import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import Controller

class Registration(QWidget):
    def __init__(self):
        self.width = 800
        self.height = 500
        super().__init__()

        self.controller = Controller.Controller()

        self.initUi()


    def createWindow(self):

        self.lineFirstName = QLineEdit()
        self.lineFirstName.setPlaceholderText("Имя ...")

        self.lineLastName = QLineEdit()
        self.lineLastName.setPlaceholderText("Фамилия ...")

        self.lineMiddleName = QLineEdit()
        self.lineMiddleName.setPlaceholderText("Отчество ...")

        self.lineTrainerLastName = QLineEdit()
        self.lineTrainerLastName.setPlaceholderText("Фамилия тренера ...")

        self.checkTrainer = QRadioButton("Тренер")
        self.checkClient = QRadioButton("Клиент")

        registrationButton = QPushButton("Зарегистрироваться")
        registrationButton.clicked.connect(self.refistrationFunc)


        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.lineFirstName)
        self.vbox.addWidget(self.lineLastName)
        self.vbox.addWidget(self.lineMiddleName)
        self.vbox.addWidget(self.lineTrainerLastName)
        self.vbox.addWidget(self.checkTrainer)
        self.vbox.addWidget(self.checkClient)
        self.vbox.addWidget(registrationButton)

        self.setLayout(self.vbox)

    def refistrationFunc(self):
        list = []
        if self.checkClient.isChecked():
            list.append(self.lineFirstName.text())
            list.append(self.lineLastName.text())
            list.append(self.lineMiddleName.text())
            ID = self.controller.insertClient(list)
        else:
            list.append(self.lineFirstName.text())
            list.append(self.lineLastName.text())
            list.append(self.lineMiddleName.text())
            ID = self.controller.insertTrainer(list)

        QMessageBox.information(self, 'Информация', 'Ваш ID = {0}'.format(str(ID)))
        self.close()


    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Регистрация')

        self.createWindow()



    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
