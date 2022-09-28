
import sys
from curses import window
from time import sleep, time

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QProgressBar,
                             QPushButton, QSplashScreen, QWidget)


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        pixmap = QPixmap("img/fundo.jpg")
        self.setPixmap(pixmap)
        QTimer.singleShot(4000, app.quit)

    def progress(self):
        for i in range(101):
            sleep(0.05)
            self.progressBar.setValue(i)

class Main(QDialog):
    def __init__(self,):
        super(QDialog, self).__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()



    sys.exit(app.exec_())
