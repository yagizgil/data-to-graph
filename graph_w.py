from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class GraphWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setUI()
        
    def setUI(self):
         h = QHBoxLayout()
         v = QVBoxLayout()
         
         #-----------
         options_h = QHBoxLayout()
         
         self.axis_x = QComboBox()
         
         self.axis_y = QComboBox()
         
         self.graph_type = QComboBox()
         self.graph_type.addItems(["plot","scatter","bar"])
         
         self.graph = QPushButton("Graph")
         self.graph.clicked.connect(self.addG)
         
         options_h.addWidget(self.axis_x)
         options_h.addWidget(self.axis_y)
         options_h.addWidget(self.graph_type)
         options_h.addWidget(self.graph)
         #---------------------------------
         v.addLayout(options_h)
         
         self.sc = Scroll()
         v.addWidget(self.sc)
         
         
         
         h.addLayout(v)
         self.setLayout(h)
        
    def addG(self):
        x = self.parent().widget(0).d[self.axis_x.currentText()]
        y = self.parent().widget(0).d[self.axis_y.currentText()]
        kind = self.graph_type.currentText()
        self.sc.addGraph(x, y, kind)


class Scroll(QScrollArea):
    
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setUI()
    
    def setUI(self):
        w = QWidget()
        self.f = QFormLayout()
        
        w.setLayout(self.f)
        self.setWidget(w)
        
    def addGraph(self,x,y,kind):
        self.f.addRow(Graph(x, y, kind))
        

class Graph(QWidget):
    
    def __init__(self,x,y,kind):
        super().__init__()
        self.xx = x
        self.yy = y
        self.kind = kind
        self.setFixedHeight(700)
        self.setUI()
    
    def setUI(self):
        self.canvas = MplCanvas()
        tool = NavigationToolbar(self.canvas, self)
        
        layout = QVBoxLayout()
        layout.addWidget(tool)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        self.plot()
    
    def plot(self):
        if self.kind == "plot":
            self.canvas.axes.plot(self.xx,self.yy)
        elif self.kind == "scatter":
            self.canvas.axes.scatter(self.xx,self.yy)
        elif self.kind == "bar":
            self.canvas.axes.bar(self.xx,self.yy)
        
        
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=200):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super().__init__(fig)