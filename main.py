from PyQt5 import QtWidgets, QtCore, uic
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
#from ui import Ui_MainWindow
import statistics # fi 7aga msh mazboota
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import matplotlib.backends.backend_pdf
ptr = 0



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('dsp2.ui', self)
        
        # self.ui = Ui_MainWindow() 
        # self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(150)
        self.timer.timeout.connect(self.update_plot_data)
        # calling browse_files function when browse button is clicked
        self.Browse_Button.clicked.connect(self.browse_files)
        self.Save_Button.clicked.connect(self.save)  

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
        # defining statistics variables
        self.mean = 0
        self.std_dev = 0
        self.min_amplitude = 0
        self.max_amplitude = 0
        self.duration = 0   # sill needs fixing
        self.maxWindow = 1
        self.play_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.OK_button.clicked.connect(self.change_color)
        self.horizontalScrollBar.setMaximum(len(self.x_csv))
        self.horizontalScrollBar.setValue(0)
        self.pen = pg.mkPen(color=(255, 255, 255))
        self.data_line = self.signals_plot_widget.plot([0], [0], pen=self.pen)
        

    def change_color(self):
        
        if self.Color_button.currentText() == "Blue":
            self.pen = pg.mkPen(color=(0, 0, 255))
        elif self.Color_button.currentText() == "Red":
            self.pen = pg.mkPen(color=(255, 0, 0))
        elif self.Color_button.currentText() == "Green":
            self.pen = pg.mkPen(color=(0, 255, 0))
        elif self.Color_button.currentText() == "White":
            self.pen = pg.mkPen(color=(255, 255, 255))

        self.data_line = self.signals_plot_widget.plot([0], [0], pen=self.pen)

    def browse_files(self):  # Browsing files function
        files_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open only txt or CSV or xls', os.getenv('HOME'),
                                                           "csv(*.csv);; text(*.txt) ;; xls(*.xls)")
        path = files_name[0]
        if pathlib.Path(path).suffix == ".txt":
            data = np.genfromtxt(path, delimiter=',')
            x = data[:, 0]
            y = data[:, 1]
            self.data = data
            self.x_txt = list(x[:])
            self.y_txt = list(y[:])
            

        elif pathlib.Path(path).suffix == ".csv":
            data = np.genfromtxt(path, delimiter=' ')
            x = data[:, 0]
            y = data[:, 1]
            self.data = data
            self.x_csv = list(x[:])
            self.y_csv = list(y[:])
            self.horizontalScrollBar.setMaximum(int(max(self.x_csv)))
            self.signals_plot_widget.setYRange(min(self.y_csv),max(self.y_csv))
            self.timer.start()


        elif pathlib.Path(path).suffix == ".xls":
            data = np.genfromtxt(path, delimiter=',')
            x = data[:, 0]
            y = data[:, 1]
            self.x_xls = list(x[:])
            self.y_xls = list(y[:])
        

    def update_plot_data(self):
        global ptr
   
        if ptr <= 40:

            self.data_line.setData(self.x_csv[0:ptr], self.y_csv[0:ptr])  # Update the data.
            self.signals_plot_widget.setXRange(0, self.x_csv[ptr] )

        else:
            self.data_line.setData(self.x_csv[0:ptr], self.y_csv[0:ptr])
            self.signals_plot_widget.setXRange(self.x_csv[ptr - 40], self.x_csv[ptr - 1])

        ptr += 1
       

    def data_stats(self, amplitude, time): # function to calculate stats for exporting to pdf
        self.mean =statistics.mean(amplitude)
        self.std_dev = statistics.stdev(amplitude)
        self.min_amplitude = min(amplitude)
        self.max_amplitude = max(amplitude)
        self.duration = max(time)
        return self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration #self.mean, self.std_dev,

    def getFigure(self): # for exporting to pdf
        fig = plt.figure(figsize=(10, 5))
        plt.plot(self.x_csv, self.y_csv)
        return fig

    def save(self):
        document = SimpleDocTemplate("report.pdf", pagesize=letter)
        items = [] 
        #self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration = self.data_stats(self.y_txt,self.x_txt)     
        self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration = self.data_stats(self.y_csv, self.x_csv) 
        # self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration = self.data_stats(self.y_xls, self.x_xls) 
        data= [['','Mean', 'Standard Deviation', 'Minimum', 'Maximum', 'Duration'],
        ['Channel 1',self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration]]
        # ['Channel 2',self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration],
        # ['Channel 3',self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration]]
        t=Table(data,6*[1.5*inch], 2*[0.5*inch])
        t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'CENTER'),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),]))
        items.append(t)
        document.build(items)

        pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
        pdf.savefig(self.getFigure())
        pdf.close()

        # report = PdfPages('figures.pdf') # make user choose name(?)
        # for signal in self.signals:
        #     report.savefig(signal.getFigure())
        #     report.savefig(signal.getSpectrogram())
        # report.close()

    def start(self):
        self.timer.start(150)

    def stop(self):
        self.timer.stop()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()
        

           
    
app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
