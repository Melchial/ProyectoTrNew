import cv2
import math
from deep_translator import MyMemoryTranslator
from loguru import logger
import time
import deepl
import os
import easyocr
from PIL import Image
# from addText import add_text_to_image
try:
    import translators.server as ts
except ModuleNotFoundError:
    import translators as ts
import RectangleManipulation as rm
from PyQt5.QtCore  import QRect



class MangaBag:
    
    def chronos(func):
        def get_time(*args, **kawrgs):
            start = time.time()
            x = func(*args, **kawrgs)
            end = time.time()
            name = ""
            if "get_text" in str(func):
                name = "EasyOcr"
            elif "get_japanese" in str(func):
                name = "MangaOcr"
            else:
                name = "Translator"
            logger.info("{} took {} seconds".format(name, (end-start)))
            return x
        return get_time
    

    
    def get_japanese(self, image, mocr, diction, direct):
        print (diction)
        if diction == {}:
            return {}
        newList = {}
        et = {}
        ts = {}
        directory = direct
        tt = []
        for x in diction:
            rectP = diction[x]
            # print(type(rectP))
            if isinstance(rectP, QRect):
                rectF= rm.getQuadfromRect(rectP)
            else:
                rectF = rectP 
            # print(rectP)
            # print(rectF)
            # cropped_image = image[abs(diction[x][0][1]):abs(diction[x][1][1]), abs(diction[x][0][0]):abs(diction[x][1][0])]
            cropped_image = image[abs(rectF[0][1]):abs(rectF[1][1]), abs(rectF[0][0]):abs(rectF[1][0])]
            # print(diction[x][0][1])
            try:
                cv2.imwrite(os.path.join(directory, str(x)+'.jpg'), cropped_image)
            except:
                logger.exception("Failed cropping!")
            et[str(x)] = os.path.join(directory, str(x)+'.jpg')
        for root, dirs, files in os.walk(directory):
            for x in files:
                try:
                    img = Image.open((root+"\\"+ x).strip())
                    text = mocr(img)
                    ts[(root+"\\"+ x).strip()] = text
                except:
                    logger.exception("File Mystery")
        mg = et.items()
        tg = ts.items()
        for coor, direct in mg:
            for dir1, jap in tg:
                if direct == dir1:
                    newList[coor] = jap
        return newList

    # def get_text(self, image):
    #     reader = easyocr.Reader(['ja'], gpu=True)  #cambiar soporte para GPU
    #     result = reader.readtext(image, paragraph=True, x_ths=.01, y_ths=.01)
    #     myDict = {}
    #     num = 0
    #     for (bbox, text) in result: 
    #         (tl, tr, br, bl) = bbox
    #         tl = (int(tl[0]), int(tl[1]))
    #         tr = (int(tr[0]), int(tr[1]))
    #         br = (int(br[0]), int(br[1]))
    #         bl = (int(bl[0]), int(bl[1]))
    #         if tl[0] < 0 or tl[1] < 0:
    #             tl = (abs(tl[0]), abs(tl[1]))
    #         if br[0] < 0 or br[1] <0:
    #             br = (abs(br[0]), abs(br[1]))
    #         # myDict[f"image{num}"] = ([tl , br ]) #se cambia para la simplicidad
    #         myDict[f"{num}"] = ([tl , br ])
    #         num += 1
    #     secDic = myDict.copy()
    #     dupKey = []
    #     #this try to delete any box in collision with another box
    #     for rect in myDict: 
    #         for key in secDic:
    #             b = secDic[key]
    #             if myDict[rect] == b:
    #                 continue
    #             else:
    #                 if myDict[rect][0][0] >= b[0][0] and myDict[rect][0][1] >= b[0][1] and myDict[rect][1][0]<= b[1][0] and myDict[rect][1][1] <= b[1][1]:
    #                     dupKey.append(rect)
    #     for x in dupKey:
    #         try:
    #             del myDict[x]
    #         except:
    #             continue

    #     return myDict
    
    def translate(self, original, name, language):
        if original == {}:
            return {}
        source = language
        if name == "DeepL":
            for key in original:
                original[key] = deepl.translate(source_language="JA", target_language="EN", text=original[key])
            return original
        elif name == "MyMemory":
            for key in original:
                original[key] = MyMemoryTranslator(source="ja", target='en').translate(original[key])
            return original
        elif name == "Google":
            for jap in original:
                original[jap] = str(ts.google(original[jap]))
            return original
        elif name == "Bing":
            for jap in original:   
                original[jap] = str(ts.bing(original[jap]))
            return original
        elif name == "Youdao":
            for jap in original:
                original[jap] = str(ts.youdao(original[jap]))
                time.sleep(5)
            return original
    
    # def addNewLine(self, img, engDict, rectDict, font, scale, thickness):
    #     newDict = {}
    #     for key in rectDict:
    #         coordinate, coordinate1 = tuple(rectDict[key])
    #         x, y = coordinate
    #         x1, y1 = coordinate1
    #         newDict[key] = self.wrap_text_in_rectangle(img, engDict[key], x, y, (x1-x), (y1-y), font, scale, thickness)
    #     return newDict

    def wrap_text_in_rectangle(self, image, text, x, y, width, height, font_face, font_scale, thickness):
        # Get the text size
        (text_width, text_height), _ = cv2.getTextSize(text, font_face, font_scale, thickness)

        # Calculate the number of lines needed to fit the text within the rectangle
        lines = []
        line = ""
        for word in text.split(" "):
            if cv2.getTextSize(line + word, font_face, font_scale, thickness)[0][0] <= width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)

        return "\n".join(lines)




    
    def write(self, img, dict1, list1, font, thick):
        if dict1 == {}:
            return img
        for value in dict1:
            try:
                cv2.rectangle(img, dict1[value][0], dict1[value][1], (0, 255, 255), 2)
                image = add_text_to_image(
                    img,
                    list1[value],
                    font_color_rgb=(255, 0, 0),
                    top_left_xy=(dict1[value][0][0], dict1[value][0][1]),
                    font_scale= font,
                    font_face=cv2.FONT_HERSHEY_DUPLEX,
                    bg_color_rgb=(255, 255, 255),
                    font_thickness=thick
                    )
            except:
                logger.exception("Mystery")
                continue
        return image