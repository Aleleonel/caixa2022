import os
import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from typing_extensions import Self


class MeuExample(QWidget):

	def __init__(self):
		super().__init__()
        
		# calling initUI method
		self.initUI()        

	# method for creating widgets
	def initUI(self):

		# creating progress bar
		self.pbar = QProgressBar(self)

		# setting its geometry
		self.pbar.setGeometry(30, 40, 200, 25)

		# creating push button
		self.btn = QPushButton('Start', self)

		# changing its position
		self.btn.move(40, 80)

		# adding action to push button
		# self.btn.clicked.connect(self.doAction)

		# setting window geometry
		self.setGeometry(300, 300, 280, 170)

		# setting window action
		self.setWindowTitle("Python")

		# showing all the widgets
		self.show()
        


	# when button is pressed this method is being called
	def doAction(self):

		# setting for loop to set value of progress bar
		for i in range(101):

			# slowing down the loop
			time.sleep(0.05)

			# setting value to progress bar
			self.pbar.setValue(i)


class LoginForm(QDialog):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setWindowTitle('Login')
        self.resize(500, 120)

        layout = QGridLayout()

        label_nome = QLabel('<font size="4"> Usuário </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Nome de Usuário')
        layout.addWidget(label_nome, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_senha = QLabel('<font size="4"> Senha </font>')
        self.lineEdit_senha = QLineEdit()
        self.lineEdit_senha.setPlaceholderText('sua senha aqui')
        layout.addWidget(label_senha, 1, 0)
        layout.addWidget(self.lineEdit_senha, 1, 1)

        # creating progress bar
        self.pbar = QProgressBar(self)
        layout.addWidget(self.pbar, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        button_login = QPushButton('Login')
        button_login.setStyleSheet('font-size: 20px; height: 30px;')
        button_login.clicked.connect(self.check_senha)
        layout.addWidget(button_login, 3, 0, 1, 1)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def check_senha(self):

        msg = QMessageBox()

        usuario = self.lineEdit_username.text()
        senha = self.lineEdit_senha.text()   
        print(usuario, senha)

        for i in range(101):
            time.sleep(0.01)
            self.pbar.setValue(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)

if QDialog.Accepted:
    form = LoginForm()
    form.show()

sys.exit((app.exec_()))
