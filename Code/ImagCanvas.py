from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt,QObject
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor, QTextOption, QFont, QCursor
from loguru import logger
from dataTranslate import DataTranslate
import copy
from loggi import logObj

class Image(QtWidgets.QLabel):
    
    
    def __init__(self, parent):
        super(Image, self).__init__(parent=parent)
        self.setPixmap(QtGui.QPixmap("F:/Proyectos/ProyectosTranslate/ProyectoTrmg/CopiaProyectoTr/Icons/whiteBG.jpg"))
        self.image = QPixmap("F:/Proyectos/ProyectosTranslate/ProyectoTrmg/CopiaProyectoTr/Icons/whiteBG.jpg")
        self.begin = QPoint()
        self.end = QPoint()
        self.color = {
            "White" : QColor(255, 255, 255),
            "Black" : QColor(0, 0, 0),
            "Red" : QColor(255, 0, 0),
            "Blue" : QColor(0, 0, 255),
            "Green" : QColor(0, 255, 0)
        }
        self.lineColor = "Blue"
        self.isPressed = False
        self.showRect = True
        self.dataTImg = DataTranslate()
        self.imgQOrig = {}
        self.imgQRect = {}

    def resetImg (self):
        self.image = QPixmap("F:/Proyectos/ProyectosTranslate/ProyectoTrmg/CopiaProyectoTr/Icons/whiteBG.jpg")
        self.setPixmap(self.image)

    def refreshImg (self):
        self.refactor()
        self.update()

    def updateImg (self, image):
        self.imFile = image
        self.image = QPixmap (image)
        self.setPixmap (self.image)
    
    def actfactor (self):
        pixWidth = self.image.width()
        pixHeight = self.image.height()
        self.factX =  float(self.frameGeometry().width())/float(pixWidth)
        self.factY = float(self.frameGeometry().height())/float(pixHeight)   

    def rectFactor (self, qRect, invers=False):
        factX = self.factX
        factY = self.factY
        if invers:
            factX = float(1)/factX
            factY = float(1)/factY    
        newX = int(qRect.x() * factX)
        newY = int(qRect.y() * factY)
        newWidth = int(qRect.width() * factX)
        newHeight = int(qRect.height() * factY)
        qRectNew = QRect( newX,newY,newWidth,newHeight)
        # print(factX)
        # print(factY)
        return(qRectNew)
    
    def refactor (self):
        if self.dataTImg.dataTextPosition:
            # print("refactor")
                # print("copia todo")
                # print(self.pages)
                # print(self.pagesRect)
            self.imgQOrig = copy.deepcopy(self.dataTImg.dataTextPosition[self.dataTImg.dataFiles[self.dataTImg.index]])
            self.imgQRect = {}
            # logObj(self.imgQOrig)
            # print(self.pages)
            # print(self.pagesRect)
            self.actfactor()
            # self.imgQRect = copy.deepcopy(self.pages[self.img])         
            # print(self.factX)
            # print(self.factY)
                            # print(self.pagesRect[self.img][f])
            for f in self.imgQOrig:
                self.imgQRect[f] = self.rectFactor(self.imgQOrig[f])

    @logger.catch
    def paintEvent(self, event):
        super().paintEvent(event)
        # print("paint event")
        # print(self.pages)
        # print(self.pagesRect)
        qp = QPainter(self)
        qp.setPen(QPen(self.color[self.lineColor], 2, Qt.SolidLine))

        # print (self.imgQOrig)
        if self.dataTImg.dataTextPosition:
            # logObj(self.imgQOrig)
            if self.imgQOrig != self.dataTImg.dataTextPosition[self.dataTImg.dataFiles[self.dataTImg.index]] and self.imgQOrig:
                self.refactor()

            if self.imgQRect:
                    # if qrectInd == {}:
                        # self.refactor()     
                    for f in self.imgQRect:
                        # if qrectInd[f]!= self.pages[self.img][f] or qrectInd[f] == None :
                        # print (self.imgQRect[f])
                        qp.drawRects(self.imgQRect[f])

        if not self.begin.isNull() and not self.end.isNull():
                # a=1
            qp.drawRect(QRect(self.begin, self.end).normalized())
    
    @logger.catch
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refactor()
      
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        #  self.setCursor(QCursor(Qt.ArrowCursor))
        self.isPressed = True
        self.begin = self.end = event.pos()
        self.update()

    @logger.catch
    def mouseMoveEvent(self, event):         
        super().mouseMoveEvent(event)
        self.end = event.pos()
        self.update()
            
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.begin = self.end = QPoint()
        self.isPressed=False
        # self.refactor()
        self.update()
        
