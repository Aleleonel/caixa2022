import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *


class Window(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        self.acceptDrops() 
        self.setWindowTitle("Image") 
        self.setGeometry(0, 0, 400, 300) 
        self.label = QLabel(self) 
        
        self.pixmap = QPixmap("img/fundo.jpg")
        self.label.setPixmap(self.pixmap) 
        self.label.resize(self.pixmap.width(), 
                          self.pixmap.height()) 
        self.show() 


App = QApplication(sys.argv) 
window = Window() 
sys.exit(App.exec()) 
