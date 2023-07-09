import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QColor, QTextOption, QFont, QPen

from trwin_ui import Ui_MainWindow
from loguru import logger
from ImagCanvas import Image

from PyQt5.QtCore import QThreadPool

from pathlib import Path
from dataTranslate import DataTransalate

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

        self.dataTranslate = DataTransalate()

        self.thread = QThreadPool()
        
    
    def appMod(self):
        self.im = Image(self.imgWidgetContainer_2)
        self.im.setScaledContents(True)

    def widgetSizes(self):
        self.imgWidgetContainer_2.setMaximumSize(QtCore.QSize(1024,960))

    def app_launch(self):
        self.locationFiles = ''

    def buttonConnections(self):
        self.buttonUpFiles.clicked.connect(self.upload1)
        self.buttonDetectPos.clicked.connect(self.detectTextPosition)

        self.horizontalLayout.addWidget(self.im)

    def upload1(self):
        print("up")
        filenames, _ =  QFileDialog.getOpenFileNames(
            None,
            "QFileDialog.getOpenFileNames()",
            "",
            "Image files (*.jpg *.png)"
        )
        if filenames != []:
            self.dataTranslate.dataFileFolder= Path( filenames[0]).parent

            self.dataTranslate.dataClear()
            self.index = 0
            self.dataTranslate.loadFiles(filenames)
            self.showImage()

            # if self.dataTranslate.dataFiles != [] and self.isBlocked:
            #     self.files.clear()
            #     self.index = 0
            #     self.isBlocked = False
            #     # self.im.pages.clear()
            #     # self.im.japanese.clear()
            #     # self.im.translated.clear()
            #     # self.im.connectDict.clear()
            #     # self.recycle.clear()
            #     self.num = -1
            #     # self.handling.deleteFiles(self.setting.Translated)
            # for file in filenames:
            #     self.files.append(file)
            # if self.files != []:
            #     self.im.img = self.files[0]
            #     if self.isSort:
            #         self.fileSorting()
            #     self.showImage()
            # if self.isClicked == False:
            #     self.translatedFiles.clear()
            #     self.saveButton.hide()
            #     self.changeTranslation.clear()
            #     self.newIndex = 0
    
    def detectTextPosition(self):
        self.im.resetImg()

    
    @logger.catch
    def showImage(self):
        # self.saveButton.show()

        im = self.dataTranslate.getDataFiles(self.index)
        pix = QPixmap(im)
        self.im.setPixmap(pix)

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())