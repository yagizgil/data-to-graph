from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
from qt_material import apply_stylesheet

import data_w as dw
import graph_w as gw

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Data to Graph")
        self.setUI()
        
    def setUI(self):
        w = QWidget()
        v = QVBoxLayout()
        h = QHBoxLayout()
        
        sp = QSplitter(Qt.Horizontal)
        
        self.menu = dw.DataWidget()
        self.screen = gw.GraphWidget()
        
        sp.addWidget(self.menu)
        sp.addWidget(self.screen)

        h.addWidget(sp)
        
        v.addLayout(h)
        w.setLayout(v)
        self.setCentralWidget(w)
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    
    w = Window()
    w.show()
    
    sys.exit(app.exec())