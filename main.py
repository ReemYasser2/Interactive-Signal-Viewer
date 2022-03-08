from pickle import GLOBAL
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QSlider
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import statistics # fi 7aga msh mazboota
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import matplotlib.backends.backend_pdf
import pandas as pd
ptr = 0
speed = 1
x_axis0 = [0,0]
y_axis0 = [0,0]
x_axis1 = [0,0]
y_axis1 = [0,0]
x_axis2 = [0,0]
y_axis2 = [0,0]



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        #Load the UI Page
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('dspxc2.ui', self)
        # defining variables for plot
        self.counter = 0
        self.max_time = 0.12
        self.max_time_init= 0
        # defining lists of amplitude and time, x and y respectively
        self.x_csv = []
        self.y_csv = []
        # defining statistics variables
        self.mean = 0
        self.std_dev = 0
        self.min_amplitude = 0
        self.max_amplitude = 0
        self.duration = 0   
        self.maxWindow = 1
        
        # self.ui = Ui_MainWindow() 
        # self.ui.setupUi(self)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(150)
        self.timer.timeout.connect(self.update_plot_data)

        self.Browse_Button.clicked.connect(self.browse_files)
        self.Save_Button.clicked.connect(self.save)  
        self.play_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)
        self.horizontalScrollBar.setMaximum(len(self.x_csv))
        self.horizontalScrollBar.setValue(0)
        self.speed_up_button.clicked.connect(self.speed_up)
        self.speed_down_button.clicked.connect(self.speed_down)
        self.pen = pg.mkPen(color=(255, 255, 255))
        self.pencolor_channel=['g','g','g']
        global ChanneloneSelected
        global ChannelTwoSelected
        global ChannelThreeSelected
        self.ChannelTwoSelected = False
        self.ChannelThreeSelected = False
        self.ChanneloneSelected= False
        self.show0=True
        self.show1=True
        self.show2=True
        self.Show_Button.clicked.connect(self.Show_signals)
        
       
        
        self.Hide_Button.clicked.connect(self.Hide_signals)
        
       # self.data_line = self.signals_plot_widget.plot([0], [0], pen=self.pencolor_channel[0])
        #self.signals_plot_widget.plot([0], [0],pen=self.pencolor_channel[0]).setData(x_axis0[0:(ptr * speed)], y_axis0[0:(ptr * speed)])
        

        

    def browse_files(self):  # Browsing files function
        files_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open only CSV ', os.getenv('HOME'), "csv(*.csv)")
        path = files_name[0]
        
        pathlib.Path(path).suffix == ".csv"
        data = pd.read_csv(path)
        self.y_csv = data.values[:, 1]
        self.x_csv = data.values[:, 0]
        global x_axis0
        global y_axis0
        global x_axis1
        global y_axis1
        global x_axis2
        global y_axis2
            
        if int(self.channel_combobox.currentIndex()) == 0:
         x_axis0=self.x_csv
         y_axis0=self.y_csv
         self.ChanneloneSelected = True
         self.horizontalScrollBar.setMaximum(int(max(x_axis0)))
         #self.signals_plot_widget.setYRange(min(x_axis0),max(y_axis0))
         self.timer.start()
         
        elif int(self.channel_combobox.currentIndex()) == 1:
         x_axis1=self.x_csv
         y_axis1=self.y_csv
         self.ChannelTwoSelected = True
         self.horizontalScrollBar.setMaximum(int(max(x_axis1)))
         #self.signals_plot_widget.setYRange(min(x_axis1),max(y_axis1))
         self.timer.start()
         
         
        elif int(self.channel_combobox.currentIndex()) == 2:
         x_axis2=self.x_csv
         y_axis2=self.y_csv
         self.ChannelThreeSelected = True
         self.horizontalScrollBar.setMaximum(int(max(x_axis2)))
         #self.signals_plot_widget.setYRange(min(x_axis2),max(y_axis2))
         self.timer.start()

        self.signals_plot_widget.setYRange(-1,1)
              

    def update_plot_data(self):
        global ptr, speed
        self.pencolors=['b','r','g']
        #currentcolor = str(self.Color_button.currentText())
        global colorindex
        if self.channel_combobox.currentIndex()==0:
            colorindex = int(self.Color_button.currentIndex())
            self.pencolor_channel[0]=self.pencolors[colorindex]
        elif self.channel_combobox.currentIndex()==1:
            colorindex = int(self.Color_button.currentIndex())
            self.pencolor_channel[1]=self.pencolors[colorindex]      
        elif self.channel_combobox.currentIndex()==2:
            colorindex = int(self.Color_button.currentIndex())
            self.pencolor_channel[2]=self.pencolors[colorindex]
        self.signals_plot_widget.clear()
        

        
        
        if ptr <= 15:
            self.signals_plot_widget.setXRange(0, x_axis0[(ptr * speed)] )
            if self.ChanneloneSelected==True and self.show0==True:
             
             self.signals_plot_widget.plot([0], [0],pen=self.pencolor_channel[0]).setData(x_axis0[0:(ptr * speed)], y_axis0[0:(ptr * speed)])  # Update the data.
            if self.ChannelTwoSelected==True and self.show1==True:
            
               self.signals_plot_widget.plot([0], [0],pen=self.pencolor_channel[1]).setData(x_axis1[0:(ptr * speed)], y_axis1[0:(ptr * speed)])  # Update the data.
            if self.ChannelThreeSelected==True and self.show2==True:
               self.signals_plot_widget.plot([0], [0],pen=self.pencolor_channel[2]).setData(x_axis2[0:(ptr * speed)], y_axis2[0:(ptr * speed)])  # Update the data.
            
                     
                
        else:
            self.signals_plot_widget.setXRange(x_axis0[(ptr * speed) - 15], x_axis0[(ptr * speed) - 1])
            if self.ChanneloneSelected==True and self.show0==True:
               self.signals_plot_widget.plot([0], [0],pen=self.pencolor_channel[0]).setData(x_axis0[0:(ptr * speed)], y_axis0[0:(ptr * speed)])           
            if self.ChannelTwoSelected==True and self.show1==True:
                self.signals_plot_widget.plot([0], [0],pen=self.pencolor_channel[1]).setData(x_axis1[0:(ptr * speed)], y_axis1[0:(ptr * speed)])
            if self.ChannelThreeSelected==True and self.show2==True:
                self.signals_plot_widget.plot([0], [0],pen=self.pencolor_channel[2]).setData(x_axis2[0:(ptr * speed)], y_axis2[0:(ptr * speed)])
       
        ptr += 1

    def Hide_signals(self):
      self.signals_plot_widget.clear()
     
      if self.ChanneloneSelected==True:
         self.show0=False
      elif self.ChannelTwoSelected==True:
          self.show1=False  
      elif self.ChannelTwoSelected==True:
         self.show2=False  

    def Show_signals(self) :
       
      if self.ChanneloneSelected==True:
         self.show0=True
      elif self.ChannelTwoSelected==True:
         self.show1=True
      elif self.ChannelTwoSelected==True:
         self.show2=False  
           
    def speed_up(self):
        global speed
        speed += 5

    def speed_down(self):
        global speed
        if speed > 1:
            speed -= 5
        else: 
            speed = 1
 

    def data_stats(self, amplitude, time): # function to calculate stats for exporting to pdf
        self.mean =statistics.mean(amplitude)
        self.std_dev = statistics.stdev(amplitude)
        self.min_amplitude = min(amplitude)
        self.max_amplitude = max(amplitude)
        self.duration = max(time)
        return self.mean, self.std_dev, self.min_amplitude, self.max_amplitude, self.duration 

    def get_channel1(self): # for exporting to pdf
        global x_axis0
        global y_axis0
        fig = plt.figure(figsize=(10, 5))
        plt.plot(x_axis0, y_axis0)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        return fig
    def get_channel2(self): # for exporting to pdf
        global x_axis1
        global y_axis1
        fig = plt.figure(figsize=(10, 5))
        plt.plot(x_axis1, y_axis1)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        return fig
    def get_channel3(self): # for exporting to pdf
        global x_axis2
        global y_axis2
        fig = plt.figure(figsize=(10, 5))
        plt.plot(x_axis2, y_axis2)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        return fig

    def save(self):
        global x_axis0
        global y_axis0
        global x_axis1
        global y_axis1
        global x_axis2
        global y_axis2
        
        
        document = SimpleDocTemplate("report.pdf", pagesize=letter)
        items = [] 
        mean0, std_dev0, min_amplitude0, max_amplitude0, duration0 = self.data_stats(y_axis0, x_axis0)     
        mean1, std_dev1, min_amplitude1, max_amplitude1, duration1 = self.data_stats(y_axis1, x_axis1)
        mean2, std_dev2, min_amplitude2, max_amplitude2, duration2 = self.data_stats(y_axis2, x_axis2)

        
        data= [['','Channel 1', 'Channel 2', 'Channel 3'],
        ['Mean',mean0, mean1, mean2],
        ['Standard Deviation', std_dev0, std_dev1, std_dev2],
        ['Minimum', min_amplitude0, min_amplitude1, min_amplitude2],
        ['Maximum', max_amplitude0, max_amplitude1, max_amplitude2],
        ['Duration',duration0, duration1, duration2]]
        t=Table(data,4*[2*inch], 6*[0.5*inch])
        t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
        ('VALIGN',(0,0),(-1,-1),'CENTER'),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),]))
        items.append(t)
        document.build(items)

        pdf = matplotlib.backends.backend_pdf.PdfPages("figures.pdf")
        pdf.savefig(self.get_channel1())
        pdf.savefig(self.get_channel2())
        pdf.savefig(self.get_channel3())
        pdf.close()

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
