from DotBotImageProcessingDataTransmission import resizeImage, grayScaleFloydSteinberg, getCoordsGray, coordStringArrayCreation, sendCoordsGray
import ctypes
import qimage2ndarray
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QToolTip, QMessageBox, QLabel, QLineEdit, QWidget, QVBoxLayout)

import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt
import imutils
import math
import serial
import time
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "First Window"
        self.setFixedSize(int(user32.GetSystemMetrics(0)*.75), int(user32.GetSystemMetrics(1)*.75))


        self.pushButton1 = QPushButton("Load an Image", self)
        self.pushButton1.move(int((user32.GetSystemMetrics(0)*.75)/4), int((user32.GetSystemMetrics(1)*.75)/2))
        self.pushButton1.adjustSize()


        self.pushButton2 = QPushButton("Take Picture", self)
        self.pushButton2.move(int((3*user32.GetSystemMetrics(0)*.75)/4), int((user32.GetSystemMetrics(1)*.75)/2))
        self.pushButton2.adjustSize()

        self.pushButton1.clicked.connect(self.toggleLoadImageWindow)
        self.pushButton2.clicked.connect(self.toggleTakeImageWindow)              # <===
        self.main_window()

    def main_window(self):
        self.setWindowTitle(self.title)
        self.show()

    def toggleLoadImageWindow(self):                                             # <===
        self.w = LoadImageWindow()
        self.w.show()
        self.hide()

    def toggleTakeImageWindow(self):                                             # <===
        self.w = TakeImageWindow()
        self.w.show()
        self.hide()

class LoadImageWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("DotBot")
        self.setFixedSize(int(user32.GetSystemMetrics(0)*.75), int(user32.GetSystemMetrics(1)*.75))
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Enter Image Path:')
        self.nameLabel.move(int((user32.GetSystemMetrics(0)*.75)/4), int((user32.GetSystemMetrics(1)*.75)/2))  
        self.nameLabel.adjustSize()      
        self.line = QLineEdit(self)
        self.line.move(int((user32.GetSystemMetrics(0)*.75)/2), int((user32.GetSystemMetrics(1)*.75)/2))
        pybutton = QPushButton('Continue', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.adjustSize()
        pybutton.move(int(user32.GetSystemMetrics(0)*.65), int(user32.GetSystemMetrics(1)*.65))        

    def clickMethod(self):
        self.address = self.line.text()
        self.w = imageWindow(self.address)
        self.w.show()
        self.hide()

class imageWindow(QMainWindow):                           # <===
    def __init__(self, address):
        super().__init__()
       
        self.setWindowTitle("DotBot")
        self.setFixedSize(int(user32.GetSystemMetrics(0)*.75), int(user32.GetSystemMetrics(1)*.75))  
        self.central_widget = QWidget()               
        self.setCentralWidget(self.central_widget)    
        lay = QVBoxLayout(self.central_widget)

        label = QLabel(self)
        self.bgrImage = cv.imread(address)
        pixmap = QPixmap(address)
        
        pixmap2 = pixmap.scaled(int(user32.GetSystemMetrics(1)*.75), int(user32.GetSystemMetrics(1)*.75), Qt.KeepAspectRatio, Qt.FastTransformation)
        
        label.setPixmap(pixmap2)
        label.move(int((user32.GetSystemMetrics(0)*.75)), int((user32.GetSystemMetrics(1)*.75)))
        #self.resize(pixmap.width(), pixmap.height())

        lay.addWidget(label)

        self.widthLabel = QLabel(self)
        self.widthLabel.setText('Max Width (mm):')
        self.widthLabel.move(int((user32.GetSystemMetrics(0)*.45)), int((user32.GetSystemMetrics(1)*.36)-(.05*(user32.GetSystemMetrics(1)))))
        self.widthLabel.adjustSize()        
        self.lineWidth = QLineEdit(self)
        self.lineWidth.move(int((user32.GetSystemMetrics(0)*.52)), int((user32.GetSystemMetrics(1)*.36)-(.05*(user32.GetSystemMetrics(1)))))

        self.heightLabel = QLabel(self)
        self.heightLabel.setText('Max Height (mm):')
        self.heightLabel.move(int((user32.GetSystemMetrics(0)*.45)), int(user32.GetSystemMetrics(1)*.36)) 
        self.heightLabel.adjustSize()       
        self.lineHeight = QLineEdit(self)
        self.lineHeight.move(int((user32.GetSystemMetrics(0)*.52)), int(user32.GetSystemMetrics(1)*.36))

        self.spacingLabel = QLabel(self)
        self.spacingLabel.setText('Spacing (mm):')
        self.spacingLabel.move(int((user32.GetSystemMetrics(0)*.45)), int((user32.GetSystemMetrics(1)*.36)+(.05*(user32.GetSystemMetrics(1)))))
        self.spacingLabel.adjustSize()        
        self.lineSpacing = QLineEdit(self)
        self.lineSpacing.move(int((user32.GetSystemMetrics(0)*.52)), int((user32.GetSystemMetrics(1)*.36)+(.05*(user32.GetSystemMetrics(1)))))

        pybutton = QPushButton('Continue', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.adjustSize()
        pybutton.move(int(user32.GetSystemMetrics(0)*.65), int(user32.GetSystemMetrics(1)*.65))  
        label.show()
        

    def clickMethod(self):
        self.maxWidth = self.lineWidth.text()
        self.maxHeight = self.lineHeight.text()
        self.spacing = self.lineSpacing.text()
        self.rgbImage = cv.cvtColor(self.bgrImage, cv.COLOR_BGR2RGB)
        print('hello')
        self.w = ditheredWindow(self.rgbImage, self.maxWidth, self.maxHeight, self.spacing)
        self.w.show()
        self.hide()

class ditheredWindow(QMainWindow):                           # <===
    def __init__(self, image, maxWidth, maxHeight, spacing):
        super().__init__()
        print('loaded')
        self.setWindowTitle("DotBot")
        self.setFixedSize(int(user32.GetSystemMetrics(0)*.75), int(user32.GetSystemMetrics(1)*.75))
        self.central_widget = QWidget()               
        self.setCentralWidget(self.central_widget)    
        lay = QVBoxLayout(self.central_widget)

        self.resizedImage = resizeImage(image, int(maxWidth), int(maxHeight), int(spacing))
        self.grayImage = cv.cvtColor(self.resizedImage, cv.COLOR_RGB2GRAY)
        self.ditheredImageGray = grayScaleFloydSteinberg(self.grayImage)
        self.coords = getCoordsGray(self.ditheredImageGray, int(spacing))

        label = QLabel(self)
        
        yourQImage = qimage2ndarray.gray2qimage(self.ditheredImageGray)
        img = QPixmap(yourQImage)
        img2 = img.scaled(int(user32.GetSystemMetrics(1)*.75), int(user32.GetSystemMetrics(1)*.75), Qt.KeepAspectRatio, Qt.FastTransformation)
        
        label.setPixmap(img2)

        lay.addWidget(label)

        self.array = coordStringArrayCreation(self.coords, 50)

        self.COMLabel = QLabel(self)
        self.COMLabel.setText('COM Port (COM17):')
        self.COMLabel.move(int((user32.GetSystemMetrics(0)*.45)), int((user32.GetSystemMetrics(1)*.36)-(.075*(user32.GetSystemMetrics(1)))))
        self.COMLabel.adjustSize()        
        self.COMPort = QLineEdit(self)
        self.COMPort.move(int((user32.GetSystemMetrics(0)*.533)), int((user32.GetSystemMetrics(1)*.36)-(.075*(user32.GetSystemMetrics(1)))))

        self.numDots = QLabel(self)
        self.numDots.setText("Number of Dots: {}".format(str(len(self.coords))))
        self.numDots.move(int((user32.GetSystemMetrics(0)*.45)), int((user32.GetSystemMetrics(1)*.36)-(.025*(user32.GetSystemMetrics(1)))))
        self.numDots.adjustSize() 

        self.printTime = QLabel(self)
        self.printTime.setText("Approximate Print Time: {} Hrs".format(round(len(self.coords)/7200, 2)))
        self.printTime.move(int((user32.GetSystemMetrics(0)*.45)), int((user32.GetSystemMetrics(1)*.36)+(.025*(user32.GetSystemMetrics(1)))))
        self.printTime.adjustSize()

        self.imageDims = QLabel(self)
        self.imageDims.setText('Final dimensions: {}mm, {}mm ({}in, {}in)'.format(self.resizedImage.shape[0], self.resizedImage.shape[1], round(self.resizedImage.shape[0]/2.54, 2), round(self.resizedImage.shape[1]/2.54, 2)))
        self.imageDims.move(int((user32.GetSystemMetrics(0)*.45)), int((user32.GetSystemMetrics(1)*.36)+(.075*(user32.GetSystemMetrics(1)))))
        self.imageDims.adjustSize()

        self.pushButtonPrint = QPushButton("Print", self)
        self.pushButtonPrint.move(int(user32.GetSystemMetrics(0)*.65), int(user32.GetSystemMetrics(1)*.65))
        self.pushButtonPrint.adjustSize()
        
    
        self.pushButtonPrint.clicked.connect(self.clickMethod)  
       
       
        label.show()

    def clickMethod(self):
        self.port = self.COMPort.text()
        sendCoordsGray(self.array, self.port)
     
class TakeImageWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DotBot")
        self.setFixedSize(int(user32.GetSystemMetrics(0)*.75), int(user32.GetSystemMetrics(1)*.75))
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Take Image:')
        self.nameLabel.move(int((user32.GetSystemMetrics(0)*.75)/4), int((user32.GetSystemMetrics(1)*.75)/2))        
        self.line = QLineEdit(self)

        self.line.move(int((user32.GetSystemMetrics(0)*.75)/2), int((user32.GetSystemMetrics(1)*.75)/2))
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)      

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec())
