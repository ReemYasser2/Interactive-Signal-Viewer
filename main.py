from PyQt5 import QtWidgets, QtCore, uic
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from ui import Ui_MainWindow
import statistics


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow() 
        self.ui.setupUi(self)

        self.ui.Browse_Button.clicked.connect(self.browse_files)
        # initializing the plot
        x = []
        y = []
        pen = pg.mkPen(color=(255, 255, 255))
        self.init_plot = self.ui.signals_plot_widget.plot(x,y,pen=pen)

        # Load the UI Page
        #uic.loadUi('dsp2.ui', self)
        # -----------
        
        # defining variables for plot
        self.counter = 0
        self.max_time = 0.12
        self.max_time_init= 0
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
        


    def browse_files(self):  # Browsing files function
        self.counter = 0
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
        files_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open only txt or CSV or xls', os.getenv('HOME'),
                                                           "csv(*.csv);; text(*.txt) ;; xls(*.xls)")
        path = files_name[0]
        if pathlib.Path(path).suffix == ".txt":
            data = np.genfromtxt(path, delimiter=',')
            x = data[:, 0]
            y = data[:, 1]
            self.x_txt = list(x[:])
            self.y_txt = list(y[:])

        elif pathlib.Path(path).suffix == ".csv":
            data = np.genfromtxt(path, delimiter=' ')
            x = data[:, 0]
            y = data[:, 1]
            self.x_csv = list(x[:])
            self.y_csv = list(y[:])
            self.update_plot_data

        elif pathlib.Path(path).suffix == ".xls":
            data = np.genfromtxt(path, delimiter=',')
            x = data[:, 0]
            y = data[:, 1]
            self.x_xls = list(x[:])
            self.y_xls = list(y[:])
        
        self.ui.signals_plot_widget.setYRange(min(self.y_csv), max(self.y_csv))
        self.max_time = 0.12
        

    def update_plot_data(self):

        # min_amplitude = min(self.y_csv)
        # max_amplitude = max(self.y_csv)
        # self.ui.signals_plot_widget.setYRange(min_amplitude, max_amplitude)
        if self.counter == 0 :
            self.ui.signals_plot_widget.setXRange(0 , self.max_time)
        elif self.counter >= 450:
            self.ui.signals_plot_widget.setXRange(self.max_time_init, self.max_time)
            self.max_time = self.max_time + 0.01
            self.max_time_init = self.max_time_init + 0.01
        
        
        #self.plt = self.ui.signals_plot_widget.plot(self.x_csv, self.y_csv)
    
        pen = pg.mkPen(color=(255, 255, 255))
        self.init_plot.setData(self.x_csv[0:self.counter], self.y_csv[0:self.counter], pen= pen)
        #self.plt = self.ui.signals_plot_widget.plot(self.x_csv[0:self.counter], self.y_csv[0:self.counter], pen= pen)
        self.counter = self.counter + 1
        #print(self.y_csv)
        # print(self.y_csv[0:self.counter])
        

        

        #self.plt = self.ui.signals_plot_widget.plot(self.x_csv, self.y_csv)
        # if self.counter > 20: #max(self.x_csv):
        #     self.timer.stop()
        #     self.counter= 0
        #     self.max_time = 20
        #     self.max_time_init = 0
           
    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
