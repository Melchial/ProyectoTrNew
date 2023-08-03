from PyQt5.QtCore import QRunnable, pyqtSignal, QObject,QPoint,QRect
from FileHandling import FileHandler
from Configer import Settings
from loguru import logger

import cv2

from RectangleManipulation import *
from Translation import MangaBag

class Worker(QObject):
    result = pyqtSignal(object)
    stored = pyqtSignal(object)
    textOriginal = pyqtSignal(object)
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    booleans = pyqtSignal(object)
    lang = pyqtSignal(str)
    
    textPos = pyqtSignal(object)

class ExtractTextOriginal(QRunnable):
    
    def __init__(self, img,mocr,textposi,language):
        super(ExtractTextOriginal, self).__init__()
        self.imag1 = img
        self.setting = Settings()
        self.manga = MangaBag()
        self.handling = FileHandler()
        # self.name = translator
        self.textposi = textposi
        self.signals = Worker()
        self.directory = self.setting.cropText
        self.portions = (100 / len(self.imag1))/3
        self.cnt = 0
        self.mocr = mocr
        self.source = None if language == "auto" else language
        self.ratio = 1

    
    def run(self):
        finalJap = {}
        finalTr ={}
        try:
            for x in self.imag1:
                
                self.img1 = cv2.imread(r"{}".format(x))
                self.image = cv2.cvtColor(self.img1, cv2.COLOR_BGR2RGB)
                #gotten_text = self.LocateText(self.image)
            
            # print(type(finalRecpos))
            # print(finalRecpos)
                # self.cnt += self.portions
                # self.signals.progress.emit(self.cnt)

                textJap = self.textposi[x]
                
                textExtract = self.manga.get_japanese(self.image, self.mocr, textJap, self.directory)
                self.cnt += self.portions
                self.signals.progress.emit(self.cnt)
                # finalTextcopy = finalText.copy()
                
                finalJap[x] = textExtract
                # print(finalJap)
            
                #find the language on the first final text value
                # if self.source == None and finalText != {}:
                #     for y in list(finalText.values()):
                #         if y != []:
                #             self.source = langid.classify(y[0])[0]
                #             break
                #
                
                # newList = self.manga.translate(finalText, self.name, self.source)
                # self.cnt += self.portions
                # self.signals.progress.emit(self.cnt)
                # # pprint(newList)
                # addNewLine1 = self.manga.addNewLine(x, newList, gotten_text, cv2.FONT_HERSHEY_DUPLEX, fontSize, thickness)
                

                # final = self.manga.write(self.image, gotten_text, addNewLine1, fontSize, thickness)
                # myarray = np.array(final)
                # image = qimage2ndarray.array2qimage(myarray)
                # finalImg.append(image)
                # self.cnt += self.portions
                # backup.append((x, gotten_text, finalTextcopy))
                # self.signals.progress.emit(self.cnt)
            

        except:
            logger.exception("ERROR")
            self.signals.finished.emit()
        else:
            self.signals.textOriginal.emit(finalJap)
            self.signals.result.emit(finalTr)
            # self.signals.stored.emit(backup)
            # self.signals.booleans.emit([self.name, self.shouldCombN, self.shouldCombO, self.range])
            # self.signals.lang.emit(self.source)
            # self.signals.finished.emit()
            #print(addNewLine1)
            

        finally:
            print("deleting files")
            self.handling.deleteFiles(self.directory)
