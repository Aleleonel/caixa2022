import sys

from PyQt5 import QtWidgets


class Test(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.buttonA = QtWidgets.QPushButton('Click!', self)
        self.buttonA.clicked.connect(self.clickCallback)
        self.buttonA.move(100, 50)

        self.buttonB = QtWidgets.QPushButton('Click!', self)
        self.buttonB.clicked.connect(self.clickCallback_b)
        self.buttonB.move(100, 100)

        self.labelA = QtWidgets.QLabel(self)
        self.labelA.move(110, 200)

        self.setGeometry(100, 100, 300, 200)

    def clickCallback(self):
        self.buttonA.setEnabled(False)
        self.labelA.setText("Button is clicked")

    def clickCallback_b(self):
        self.buttonA.setEnabled(True)
        self.buttonB.setEnabled(False)
        self.labelB.setText("Button is clicked")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    test = Test()
    test.show()
    sys.exit(app.exec_())
