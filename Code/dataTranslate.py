from  pathlib import Path

class DataTranslate ():

    

    def __init__(self) :
        
        #data is cleared and initialized at once
        self.dataClear() 
        self.isSort = False
        

    def loadFiles (self, _dataFiles):
        self.isSort = False
        self.dataClear()
    
        self.dataFileFolder = str(Path(_dataFiles[0]).parent)+'\\'  
        for file in _dataFiles:
            self.dataFiles.append(Path(file).name)
        self.fileSorting()
        self.dataFilesLast =  len(self.dataFiles)-1
        # print(self.dataFiles)

    def getFiles (self, _index=-1):
        if _index< 0:
            return self.dataFiles
        else:
            return self.dataFiles[_index]
        
    def loadTextPosition (self, _dataTextPosition ):
        self.dataTextPosition = _dataTextPosition

    def getTextPosition (self, _index=-1):
        if _index< 0:
            return self.dataTextPosition
        else:
            return self.dataTextPosition[_index]

    #data is legaded       
    def showDataLog(self):    
        print (self.dataFileFolder)
        print (self.dataFiles)
        print (self.dataTextPosition)
        print (self.dataTextOriginal)
        print (self.dataTextTranslated)

    def fileSorting(self):
        if not self.isSort:
            self.dataFiles.sort()
            self.isSort = True
            # for file in self.dataFiles:
            #     sp = file.split("/")
            #     nd[sp[-1].split(".")[0]] = file
            # # pprint(nd)
            # for n in nd.keys():
            #     if n.isdigit():
            #         temp.append(int(n))
            #         conn[int(n)] = n
            #     else:
            #         conn[n] = n
            #         temp.append(n)
            # temp.sort()
            # for x in temp:
            #     sortedFiles.append(nd[conn[x]])
            # self.files = sortedFiles

    def getDataFiles (self, _index):
        if self.dataFiles != []:
            dataFile = str(Path(self.dataFileFolder).joinpath(self.dataFiles[_index]))
            return dataFile

            
            

    def dataClear(self):
        #TODO: reorganizar las propiedasdes de la clase
        # self.index = 0 
        self.dataFileFolder = ''
        self.dataFilesLast = 0
        self.dataFiles = []
        self.dataTextPosition = {}
        self.dataTextOriginal = {}
        self.dataTextTranslated = {}
        self.textPositionBool = False
        self.textOriginalBool = False
        self.textTranslatedlBool = False
