from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
import pandas as pd
import numpy as np

import sqlite3 as sql

class DataWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.setUI()
        
    def setUI(self):
        h = QHBoxLayout()
        v = QVBoxLayout()
        
        #import dataframe
        import_v = QVBoxLayout()
        first_layout_bar = QHBoxLayout()
        self.file_type = QComboBox()
        self.file_type.addItems(["read_csv","read_excel","read_json","read_sql"])
        self.file_type.currentTextChanged.connect(self.set_arg)
        
        self.file_edit = QLineEdit()
        
        self.file_open = QPushButton("Dosya Aç")
        self.file_open.setCursor(QCursor(Qt.PointingHandCursor))
        self.file_open.clicked.connect(self.set_open_file)
        
        first_layout_bar.addWidget(self.file_type)
        first_layout_bar.addWidget(self.file_edit)
        first_layout_bar.addWidget(self.file_open)
        
        import_v.addLayout(first_layout_bar)
        
        second_layout_bar = QHBoxLayout()
        self.arg_name = QLabel("sep:")
        self.csv_sep = QLineEdit(",")
        
        self.excel_sheet = QLineEdit("0")
        
        self.sql_table = QLineEdit()
        self.sql_table.setPlaceholderText("tablo adı")
        
        #----
        self.excel_sheet.setVisible(False)
        self.sql_table.setVisible(False)
        #----
        
        self.run = QPushButton("Çalıştır")
        self.run.setCursor(QCursor(Qt.PointingHandCursor))
        self.run.clicked.connect(self.set_run)
        
        second_layout_bar.addWidget(self.arg_name)
        second_layout_bar.addWidget(self.csv_sep)
        second_layout_bar.addWidget(self.excel_sheet)
        second_layout_bar.addWidget(self.sql_table)
        second_layout_bar.addWidget(self.run)
        
        import_v.addLayout(second_layout_bar)
        #-----------------------------------------------
        
        self.table = QTableView()        
        self.model = PandasModel()
        self.table.setModel(self.model)
        
        
        
        
        
        
        v.addLayout(import_v)
        v.addWidget(self.table)
        
        h.addLayout(v)
        self.setLayout(h)
    
    def set_arg(self, txt):
        if txt == "read_csv":
            self.arg_name.setVisible(True)
            self.arg_name.setText("sep:")
            self.csv_sep.setVisible(True)
            self.excel_sheet.setVisible(False)
            self.sql_table.setVisible(False)
        elif txt == "read_excel":
            self.arg_name.setVisible(True)
            self.arg_name.setText("sheet_name:")
            self.csv_sep.setVisible(False)
            self.excel_sheet.setVisible(True)
            self.sql_table.setVisible(False)
        elif txt == "read_sql":
            self.arg_name.setVisible(True)
            self.arg_name.setText("table:")
            self.csv_sep.setVisible(False)
            self.excel_sheet.setVisible(False)
            self.sql_table.setVisible(True)
        else:
            self.arg_name.setVisible(False)
            self.csv_sep.setVisible(False)
            self.excel_sheet.setVisible(False)
            self.sql_table.setVisible(False)
        
    def set_open_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        if dlg.exec_():
            file = dlg.selectedFiles()
            self.file_edit.setText(file[0])
            
            
            
    def set_run(self):
        if self.file_type.currentText() == "read_csv":
            if self.csv_sep.text() != "": self.d = pd.read_csv(self.file_edit.text(),sep=self.csv_sep.text())
            else: pass
        
        elif self.file_type.currentText() == "read_excel":
            if self.excel_sheet.text() != "0": self.d = pd.read_excel(self.file_edit.text(),sheet_name=self.excel_sheet.text())
            else: self.d = pd.read_excel(self.file_edit.text())
        
        elif self.file_type.currentText() == "read_sql":
            con = sql.connect(self.file_edit.text())
            self.d = pd.read_sql(self.sql_table.text(),con)
            con.close()
        
        else: 
            self.d = pd.read_json(self.file_edit.text())
            
        
        self.model.setData(self.d)
        
        self.parent().widget(1).axis_x.addItems(list(self.d.columns))
        self.parent().widget(1).axis_y.addItems(list(self.d.columns))
        
        

class PandasModel(QAbstractTableModel): 
    def __init__(self):
        QAbstractTableModel.__init__(self)

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
    
    def setData(self,data):
        self._data = data
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()