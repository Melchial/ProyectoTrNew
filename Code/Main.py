import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog,QStatusBar
)
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QColor, QTextOption, QFont, QPen


from trwin_ui import Ui_MainWindow
import trwin_ui
from loguru import logger
from ImagCanvas import Image

from PyQt5.QtCore import QThreadPool

from pathlib import Path
from dataTranslate import DataTranslate

from extractTextPosition import DetectTextPosi
from extractTextOrig import ExtractTextOriginal
from loggi import logObj
from jsonHandler import ( saveDataJson, loadDataJson)
class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        # super().__init__(parent)
        super(Window, self).__init__()
        self.setupUi(self)
        self.appMod()
        self.buttonConnections()
        
        self.widgetSizes()
        self.isBlocked = False
        self.im.adjustSize()

        self.dataT = DataTranslate()
        self.index =0
        self.thread = QThreadPool()
        
    
    def appMod(self):
        self.im = Image(self.imgWidgetContainer)
        self.im.setScaledContents(True)

        self.statBar = QStatusBar ()
        self.setStatusBar (self.statBar)
        self.statBar.show()

    def widgetSizes(self):
        self.imgWidgetContainer.setMaximumSize(QtCore.QSize(1024,960))

    def app_launch(self):
        self.locationFiles = ''

    def setStatMessage (self):
        message = self.dataT.dataFiles[self.index]
        message = message or ''
        # logObj(message)
        self.statBar.showMessage (message)


    def buttonConnections(self):
        self.buttonUpFiles.clicked.connect(self.uploadFiles)
        self.buttonDetectPos.clicked.connect(self.detectTextPosition)
        self.buttonLeftNavigate.clicked.connect(self.moveLeft)
        self.buttonRightNavigate.clicked.connect(self.moveRight)
        self.buttonLoadData.clicked.connect(self.loadDataT)

        self.buttonSaveData.clicked.connect (self.saveDataT)

        self.buttonSaveEdit.clicked.connect (self.testButton)
        
        self.layoutImage.addWidget(self.im)


    #Button Functions 
    def uploadFiles(self):
        print("uploading files")
        filenames, _ =  QFileDialog.getOpenFileNames(
            None,
            "QFileDialog.getOpenFileNames()",
            "",
            "Image files (*.jpg *.png)"
        )
        if filenames != []:
            self.index=0
            self.dataT.dataClear()
            self.dataT.loadFiles(filenames)
            self.showImage()
    
   
    def moveImage(self, direction):
        
        new_index = self.index+direction
        
        if  new_index < 0:
                new_index = 0
        if  new_index > self.dataT.dataFilesLast:
                new_index = self.dataT.dataFilesLast
        
        self.index= new_index

        self.setStatMessage()

        if self.dataT.dataFiles != []:
            print('updImg')
            self.showImage()
            
            #self.drawOnPages()

    def moveRight(self):
        self.moveImage(1)
        
    def moveLeft(self):
        self.moveImage(-1)


    #After Theads functions
    def afterDetectText(self):
        print ("update DataTImg")
        self.im.dataTImg= self.dataT
        self.im.refreshImg()
        # self.im.update()
        print ("finish detext text")
    
    def afterExtractText (self):
        print ("update DataTImg")

    #proper functions    
    def updatePositionText (self,_textDetected ):
        self.dataT.loadTextPosition(_textDetected)

    def testButton(self):
        self.dataT.showDataLog()
        # print(self.im.imgQOrig)
        # print(self.im.imgQRect)

    def saveDataT(self):
        saveDataJson (self.dataT)
        
    def loadDataT (self):
        self.dataT= loadDataJson("out.json")
        self.im.dataTImg=self.dataT
        self.showImage()

    @logger.catch
    def showImage(self):
        # self.saveButton.show()
        # print(self.dataT.index)
        # im = self.dataT.getDataFiles(self.dataT.index)
        # print(im)
        # pix = QPixmap(im)
        # self.im.setPixmap(pix)
        self.im.updateImg(self.dataT.getDataFiles(self.index))
        self.im.refactor()

        # self.im.update()

        # if self.isClicked and not self.im.flag and self.translatedFiles != []:
        #     self.saveButton.show()
        #     im = self.translatedFiles[self.newIndex]
        #     pix = QPixmap(im)
        #     self.im.setPixmap(pix)
        # elif self.isClicked and self.im.flag:
        #     self.drawOnPages()
        #     print(self.index)
        #     im = self.files[self.index]
        #     # print(im)
        #     pix = QPixmap(im)
        #     self.im.image = pix
        #     self.im.setPixmap(pix)

        #     self.im.refactor()
        #     self.im.actContCuad()
        #     self.im.update()
        #     self.saveButton.show()
        # else:
        #     pix = QPixmap(self.files[self.index])
        #     self.im.image = pix
        #     size = pix.size()
        #     self.clearButton.show()
        #     if size.width() > size.height():
        #         self.imageWidget.setMaximumSize(QtCore.QSize(990,680))
        #     else:
        #         self.imageWidget.setMaximumSize(QtCore.QSize(700,800))
        #     if not self.im.flag:
        #         self.im.setPixmap(self.im.image)
        #     self.drawOnPages()


    #functions for the main process
    def detectTextPosition(self):
        # self.clearButton.hide()
        if self.dataT.dataFiles:
            logger.info("Find Text Position")
            self.worker = DetectTextPosi(self.dataT,False,False)              
            self.worker.signals.result.connect(self.updatePositionText)
            self.worker.signals.finished.connect(self.afterDetectText)              
            self.thread.start(self.worker)
        else: pass
                

    def extractTextOriginal(self):
        # self.clearButton.hide()
        if self.dataT.dataTextPosition:
            logger.info("Extract Text Original")
            self.worker = ExtractTextOriginal(self.dataT,True,True)              
            self.worker.signals.result.connect(self.positionText)
            self.worker.signals.finished.connect(self.afterExtractText)              
            self.thread.start(self.worker)              
        else: pass
            


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())