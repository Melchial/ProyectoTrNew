from PyQt5.QtCore import QRunnable, pyqtSignal, QObject,QPoint,QRect
from FileHandling import FileHandler
from Configer import Settings
from loguru import logger

import cv2
import easyocr
from RectangleManipulation import *
from Translation import MangaBag

from loggi import logObj

from imgHandling import (
    getFontSizeThickness as imgGetFontSizeThickness, getRatio as imgGetRatio
)

class Worker(QObject):
    result = pyqtSignal(object)
    stored = pyqtSignal(object)
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    booleans = pyqtSignal(object)
    lang = pyqtSignal(str)
    # textPos = pyqtSignal(object)

class DetectTextPosi(QRunnable):
    
    def __init__(self, dataFiles, combN=False, combO=False, sliderNum=2):
        super(DetectTextPosi, self).__init__()
        self.dataFiles = dataFiles
        self.dataFileFolder = dataFiles.dataFileFolder
        self.setting = Settings()
        self.manga = MangaBag()
        self.fileHandling = FileHandler()
        # self.name = translator
        self.shouldCombN = combN
        self.shouldCombO = combO

        # logObj(self.dataFiles.getDataFiles(0))
     
        self.range = sliderNum * imgGetRatio(self.dataFiles.getDataFiles(0)) + 4
        self.signals = Worker()
        self.directory = self.setting.cropText
        # self.portions = (100 / len(self.imag1))/3
        self.cnt = 0
        # self.mocr = mocr
        # self.source = None if language == "auto" else language
        self.ratio = 1

    def get_textPosition(self, image):
        reader = easyocr.Reader(['ja'], gpu=True)  #cambiar soporte para GPU
        result = reader.readtext(image, paragraph=True, x_ths=.01, y_ths=.01)
        myDict = {}
        num = 0
        for (bbox, text) in result: 
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            if tl[0] < 0 or tl[1] < 0:
                tl = (abs(tl[0]), abs(tl[1]))
            if br[0] < 0 or br[1] <0:
                br = (abs(br[0]), abs(br[1]))
            # myDict[f"image{num}"] = ([tl , br ]) #se cambia para la simplicidad
            myDict[f"{num}"] = ([tl , br ])
            num += 1
        secDic = myDict.copy()
        dupKey = []
        #this try to delete any box in collision with another box
        for rect in myDict: 
            for key in secDic:
                b = secDic[key]
                if myDict[rect] == b:
                    continue
                else:
                    if myDict[rect][0][0] >= b[0][0] and myDict[rect][0][1] >= b[0][1] and myDict[rect][1][0]<= b[1][0] and myDict[rect][1][1] <= b[1][1]:
                        dupKey.append(rect)
        for x in dupKey:
            try:
                del myDict[x]
            except:
                continue

        return myDict
    

    def LocateText(self, image):
        myDict = self.get_text(image)
        # print(myDict)
        # print(self.shouldCombN)
        # print(self.shouldCombO)
        if self.shouldCombN and self.shouldCombO:
            # print(myDict)
            bound1 = rectanglesCO(myDict, "c")
            # print(bound1)
            # print(self.range)
            bound2 = combine_rectangles(bound1, self.range)
            # print(bound2)
            overlap1 = rectanglesCO(bound2, "o")
            # print(overlap1)
            overlap = combine_overlapping_rectangles(overlap1)
            # print(overlap)
            return overlap
        elif self.shouldCombN and not(self.shouldCombO):
            bound3 = rectanglesCO(myDict, "c")
            bound4 = combine_rectangles(bound3, self.range)
            return bound4
        elif self.shouldCombO and not(self.shouldCombN):
            overlap3 = rectanglesCO(myDict, "o")
            overlap4 = combine_overlapping_rectangles(overlap3)
            return overlap4
        else:
            return myDict


    def get_text(self, image):
        reader = easyocr.Reader(['ja'], gpu=True)  #cambiar soporte para GPU
        result = reader.readtext(image, paragraph=True, x_ths=.01, y_ths=.01)
        myDict = {}
        num = 0
        for (bbox, text) in result: 
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            if tl[0] < 0 or tl[1] < 0:
                tl = (abs(tl[0]), abs(tl[1]))
            if br[0] < 0 or br[1] <0:
                br = (abs(br[0]), abs(br[1]))
            # myDict[f"image{num}"] = ([tl , br ]) #se cambia para la simplicidad
            myDict[f"{num}"] = ([tl , br ])
            num += 1
        secDic = myDict.copy()
        dupKey = []
        #this try to delete any box in collision with another box
        for rect in myDict: 
            for key in secDic:
                b = secDic[key]
                if myDict[rect] == b:
                    continue
                else:
                    if myDict[rect][0][0] >= b[0][0] and myDict[rect][0][1] >= b[0][1] and myDict[rect][1][0]<= b[1][0] and myDict[rect][1][1] <= b[1][1]:
                        dupKey.append(rect)
        for x in dupKey:
            try:
                del myDict[x]
            except:
                continue

        return myDict

    def run(self):
        finalImg = []
        finalRecpos ={}
        try:
            for file in self.dataFiles.getFiles():
                # print(file)
                # fontSize, thickness = self.manga.getFontSizeThickness(file)
                # print(f"{self.dataFileFolder}{file}")
                self.img1 = cv2.imread(r"{}".format(f"{self.dataFileFolder}{file}"))
                self.image = cv2.cvtColor(self.img1, cv2.COLOR_BGR2RGB)
                gotten_text = self.LocateText(self.image)
                # pprint(gotten_text)
                # print(type(gotten_text))
                # print(gotten_text)
                # print(type(x))
                # print(x)
                finalsq = {}
                for i in gotten_text:
                    x1 = QPoint(gotten_text[i][0][0],gotten_text[i][0][1])
                    y1 = QPoint(gotten_text[i][1][0],gotten_text[i][1][1])
                    finalsq[i]=QRect(x1,y1).normalized()
                finalRecpos[file]=finalsq

            
        except:
            logger.exception("ERROR")
            self.signals.finished.emit()
        else:
            self.signals.result.emit(finalRecpos)
            self.signals.finished.emit()
            # self.signals.stored.emit(backup)
            # self.signals.booleans.emit([self.name, self.shouldCombN, self.shouldCombO, self.range])
            # self.signals.lang.emit(self.source)
            # self.signals.finished.emit()
            #print(addNewLine1)
            

        finally:
            print("finish detext text")
            # self.filefileHandling.deleteFiles(self.directory)
