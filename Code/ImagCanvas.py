from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt,QObject
from PyQt5.QtCore import Qt, QPoint, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor, QTextOption, QFont, QCursor
from loguru import logger


class Image(QtWidgets.QLabel):
    def __init__(self, parent):
        super(Image, self).__init__(parent=parent)
        self.setPixmap(QtGui.QPixmap("F:/Proyectos/ProyectosTranslate/ProyectoTrmg/CopiaProyectoTr/Icons/whiteBG.jpg"))
        self.img = None
        self.image = QPixmap("F:/Proyectos/ProyectosTranslate/ProyectoTrmg/CopiaProyectoTr/Icons/whiteBG.jpg")

    def resetImg (self):
        self.img = None
        self.image = QPixmap("F:/Proyectos/ProyectosTranslate/ProyectoTrmg/CopiaProyectoTr/Icons/whiteBG.jpg")
        self.setPixmap(self.image)