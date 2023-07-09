




class DataTransalate ():

    

    def __init__(self) :
        
        self.index = 0
        
        self.dataFileFolder = ''
        self.dataFiles = []
        self.dataTextPosition = {}
        self.dataTextOriginal = {}
        self.dataTextTranslated = {}

        self.isSort = False

    def loadFiles (self, _dataFiles):
        self.dataFiles = _dataFiles
        self.fileSorting()

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
            return self.dataFiles[_index]

    def dataClear(self):
        self.dataFileFolder = ''
        self.dataFiles = []
        self.dataTextPosition = {}
        self.dataTextOriginal = {}
        self.dataTextTranslated = {}