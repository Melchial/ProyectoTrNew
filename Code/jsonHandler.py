import json

from dataTranslate import DataTranslate
from PyQt5.QtCore import QRect


def saveDataJson (dataT: DataTranslate):
    
    dataT.index 
    dataT.dataFileFolder 
    dataT.dataFilesLast 
    dataT.dataFiles 
    dataT.dataTextPosition 
    dataT.dataTextOriginal 
    dataT.dataTextTranslated 

    textPositionBool =  True if dataT.dataTextPosition else False
    textOriginalBool =  True if dataT.dataTextOriginal else False
    textTranslatedlBool =  True if dataT.dataTextTranslated else False

    # print(textPositionBool)

    jsonDataT = []
    jsonDataT.append( {  "fileFolder"   :    dataT.dataFileFolder,
                        "longFiles"     :    len(dataT.dataFiles)-1,
                        "textPosition"  :    textPositionBool,
                        "textOriginal"  :    textOriginalBool,
                        "textTranslated":    textTranslatedlBool


                }
                )
    
    for j in dataT.dataFiles:
        dataItem = {}
        dataItem["file"]= j
        
        if textPositionBool:
            dataSubItem = {}
            for p in dataT.dataTextPosition[j]:
                qRe = dataT.dataTextPosition[j][p]
                dataSubItem[p] = (qRe.x(), qRe.y(), qRe.width(), qRe.height())
            dataItem["textPosition"]=dataSubItem
        
        if textOriginalBool:
            dataItem["textOriginal"]=dataT.dataTextOriginal
        
        if textTranslatedlBool:
            dataItem["textTranslated"]=dataT.dataTextTranslated
        
        jsonDataT.append(dataItem)

    #     jsonDataT.append({"file" : '015.jpg',
    #                     "textPosition": {   
    #                     '0':  (159, 61, 253, 163), 
    #                     '3':  (337, 315, 45, 41),
    #                     '4':  (700, 146, 99, 223), 
    #                     '5':  (173, 296, 110, 192), 
    #                     '8':  (770, 594, 59, 139), 
    #                     '10': (90, 746, 27, 147), 
    #                     '11': (119, 797, 21, 45), 
    #                     '13': (362, 970, 33, 33), 
    #                     '14': (137, 947, 84, 141), 
    #                     '15': (337, 1139, 65, 127), 
    #                     '17': (201, 1266, 76, 106), 
    #                     '18': (338, 1464, 27, 73)
    #                     },
    #                     "textOriginal" :{
    #                         '0':  "prueba1", 
    #                         '3':  "prueba2",
    #                         '4':  "prueba3", 
    #                         '5':  "prueba3", 
    #                         '8':  "prueba3", 
    #                         '10': "prueba3",  
    #                         '11': "prueba3", 
    #                         '13': "prueba3", 
    #                         '14': "prueba3", 
    #                         '15': "prueba3",  
    #                         '17': "prueba3", 
    #                         '18': "prueba3", 
    #                     }

    # }
    #  )
    # jsonDataT.append({"file" : '016.jpg',
    #                     "textPosition": {   
    #                     '0':  (159, 61, 253, 163), 
    #                     '3':  (337, 315, 45, 41),
    #                     '4':  (700, 146, 99, 223), 
    #                     '5':  (173, 296, 110, 192), 
    #                     '8':  (770, 594, 59, 139), 
    #                     '10': (90, 746, 27, 147), 
    #                     '11': (119, 797, 21, 45), 
    #                     '13': (362, 970, 33, 33), 
    #                     '14': (137, 947, 84, 141), 
    #                     '15': (337, 1139, 65, 127), 
    #                     '17': (201, 1266, 76, 106), 
    #                     '18': (338, 1464, 27, 73)
    #                     },
    #                     "textOriginal" :{
    #                         '0':  "prueba1", 
    #                         '3':  "prueba2",
    #                         '4':  "prueba3", 
    #                         '5':  "prueba3", 
    #                         '8':  "ads", 
    #                         '10': "prueba3",  
    #                         '11': "prueba3", 
    #                         '13': "prueba3", 
    #                         '14': "prueba3", 
    #                         '15': "prueba3",  
    #                         '17': "prueba3", 
    #                         '18': "prueba3", 
    #                     }

    # }
    #  )
    # print(jsonDataT)
    json.dump(jsonDataT,open("out.json","w"))

def loadDataJson ( file:str) -> DataTranslate: 
    dataO = json.loads( open(file,"r").read())
    # print (dataO)


    dataT = DataTranslate()
    
    dataT.dataFileFolder = dataO[0]["fileFolder"]
    dataT.dataFilesLast = dataO[0]["longFiles"]
    dataT.textPositionBool = dataO[0]["textPosition"]
    dataT.textOriginalBool = dataO[0]["textOriginal"]
    dataT.textTranslatedlBool = dataO[0]["textTranslated"]

    structure = {   "textPosition"  :   (dataT.textPositionBool,dataT.dataTextPosition) ,
                    "textOriginal"  :   (dataT.textOriginalBool,dataT.dataTextOriginal) ,
                    "textTranslated":   (dataT.textTranslatedlBool,dataT.dataTextTranslated)
    }
    #print(structure)
    dataO.pop(0)
    #print(dataO)

    for j in range(len(dataO)):
        # print(j)
        
        #FileN elemento j del json
        fileN = dataO[j]
        #file namefile
        file = fileN["file"]
        dataT.dataFiles.append(file)
        # print(fileN)
        
        #for each dataTipe (position, textOriginal, TextTraduc)
        for st in structure:
            dataItem = structure[st][1]
            dataItem[file]={}
            if  structure[st][0]:             
                for index in fileN[st]:
                    item = fileN[st][index]
                    dataItem[file][index] = item
                    if st == "textPosition":
                        # print (dataItem[file][index])
                        rect = dataItem[file][index]
                        dataItem[file][index] =QRect( rect[0],rect[1],rect[2],rect[3])
    # print (dataT)
    return dataT
    # print(dataT.dataTextPosition)    
    # print(dataT.dataTextOriginal) 

# datat = DataTranslate()
# saveDataJson(datat)

# dataOut = loadDataJson("out.json")


# exit()

# qRect = QRect(159, 61, 253, 163)

# jsonExample = [
#     {
#         "fileFolder" : "F:/Proyectos/TestTr",
#         "longFiles" : 3 ,
#         "textPosition" : True , 
#         "textOriginal" : True ,
#         "textTransalted" : True,
#     }
#     ,
#     {
#         "file" : '015.jpg',
#         "textPos": {   
#                     '0':  (159, 61, 253, 163), 
#                     '3':  (337, 315, 45, 41),
#                     '4':  (700, 146, 99, 223), 
#                     '5':  (173, 296, 110, 192), 
#                     '8':  (770, 594, 59, 139), 
#                     '10': (90, 746, 27, 147), 
#                     '11': (119, 797, 21, 45), 
#                     '13': (362, 970, 33, 33), 
#                     '14': (137, 947, 84, 141), 
#                     '15': (337, 1139, 65, 127), 
#                     '17': (201, 1266, 76, 106), 
#                     '18': (338, 1464, 27, 73)
#                     }

#     },
#     {
#         "file" : '016.jpg',
#         "textPos": {   
#                     '0': (577, 37, 37, 75), 
#                     '1': (636, 92, 77, 163), 
#                     '2': (176, 396, 51, 53), 
#                     '5': (207, 1021, 21, 27), 
#                     '6': (204, 1066, 27, 75), 
#                     '9': (167, 1278, 82, 113), 
#                     '10': (783, 100, 171, 296), 
#                     '11': (96, 247, 92, 130), 
#                     '12': (416, 484, 79, 78), 
#                     '13': (451, 1138, 172, 143)
#                     }

#     }



# ]


# jsonEnconde =  json.JSONEncoder().encode(jsonExample)

# print(jsonEnconde)

# jsonDecode = json.JSONDecoder().decode (jsonEnconde)


# print (jsonDecode)
