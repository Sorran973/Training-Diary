import sys

from PyQt5.QtWidgets import *

import Registration
from Client import TrainingDiaryForClient
from Trainer import TrainingDiaryForTrainer
import Controller


class Authorization(QWidget):
    def __init__(self):
        self.width = 800
        self.height = 500
        super().__init__()

        self.controller = Controller.Controller()
        # self.controller.testInsertWorkoutClient()

        self.initUi()


    def createWindow(self):
        self.lineInputID = QLineEdit()
        self.lineInputID.setPlaceholderText("Введите свой ID ...")

        self.lineInputPass = QLineEdit()
        self.lineInputPass.setPlaceholderText("Введите свой пароль ...")

        self.checkTrainer = QRadioButton("Тренер")
        self.checkClient = QRadioButton("Клиент")

        goInputButton = QPushButton("Войти")
        goInputButton.clicked.connect(self.goInputFunc)

        goRegistrationButton = QPushButton("Регистрация")
        goRegistrationButton.clicked.connect(self.goRegistrationFunc)


        vbox = QVBoxLayout()
        vbox.addWidget(self.lineInputID)
        vbox.addWidget(self.lineInputPass)
        vbox.addWidget(self.checkTrainer)
        vbox.addWidget(self.checkClient)
        vbox.addWidget(goInputButton)
        vbox.addWidget(goRegistrationButton)

        self.setLayout(vbox)

    def goInputFunc(self):
        if self.lineInputPass.text() == '123':
            QMessageBox.warning(self, 'Ошибка', 'Неверный пароль')
        else:
            if self.checkClient.isChecked():
                self.trainingDiaryForClient = TrainingDiaryForClient.TrainingDiaryForClient(self.lineInputID.text())
                self.trainingDiaryForClient.show()
                self.close()
            else:
                self.trainingDiaryForTrainer = TrainingDiaryForTrainer.TrainingDiaryForTrainer(self.lineInputID.text())
                self.trainingDiaryForTrainer.show()
                self.close()

    def goRegistrationFunc(self):
        self.registration = Registration.Registration()
        self.registration.show()


    def initUi(self):
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle('Авторизация')

        self.createWindow()

        self.show()


    def center(self):
        frameGm = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    authorization = Authorization()
    sys.exit(app.exec_())