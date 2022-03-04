from PyQt5 import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pathlib
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QAction, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from ui import Ui_MainWindow
from random import randint # just for testing


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() # Call the inherited classes __init__ method
        #self.ui.loadUi('dsp1.ui', self) # Load the .ui file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # defining lists of amplitude and time for all file types 
        self.x_txt = []
        self.y_txt = []
        self.x_csv = []
        self.y_csv = []
        self.x_xls = []
        self.y_xls = []
        # defining stats variables
        self.mean = 0
        self.std_dev = 0
        self.min_amplitude = 0
        self.max_amplitude = 0
        self.duration = 0

        
        self.x = list(range(100))  # 100 time points
        self.y = [randint(0,100) for _ in range(100)]  # 100 data points
        self.signals_plot_widget.setBackground('b')
        pen = pg.mkPen(color=(255, 0, 0)) #red
        self.data_line =  self.signals_plot_widget.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        self.ui.actionOpen.triggered.connect(self.browse_files) # when open in file in the menubar is triggered
        self.show()  # Show the GUI


    # def plot(self): # plotting Function

    #     self.signals_plot_widget.plot(self.x_csv, self.y_csv, 'g')

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0,100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.

    def browse_files(self): # Browsing files function
        files_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open only txt or CSV or xls', os.getenv('HOME'),
                                            "csv(*.csv);; text(*.txt) ;; xls(*.xls)")
        path = files_name[0]
        if pathlib.Path(path).suffix == ".txt":
            data = np.genfromtxt(path, delimiter=',')
            x = data[:, 0]
            y= data[:, 1]
            self.x_txt = list(x[:])
            self.y_txt = list(y[:])
            #self.plot()

        elif pathlib.Path(path).suffix == ".csv":
            data = np.genfromtxt(path, delimiter=' ')
            x = data[:, 0]
            y = data[:, 1]
            self.x_csv= list(x[:])
            self.y_csv = list(y[:])
            print(self.x_csv)
            print(self.y_csv)
            #self.plot()

        elif pathlib.Path(path).suffix == ".xls":
            data = np.genfromtxt(path, delimiter=',')
            x = data[:, 0]
            y = data[:, 1]
            self.x_xls = list(x[:])
            self.y_xls = list(y[:])
            #self.plot()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
#if __name__ == '__main__':




