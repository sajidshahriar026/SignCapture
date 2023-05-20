import json
import os


class DatasetDirectoryLogs():
    def __init__(self):
        self.fileName = 'dataset_directory_logs.json'

    def addToDatasetDirectoryLogs(self, baseDirectoryName):
        datasetDirectoryLogs = []
        entry = {baseDirectoryName.split('/')[-1]: {'location': baseDirectoryName}}

        if not os.path.exists(self.fileName):
            with open(self.fileName, 'w') as fileHandle:
                datasetDirectoryLogs.append(entry)
                json.dump(datasetDirectoryLogs, fileHandle, indent=4)
        else:
            try:
                with open(self.fileName, 'r') as fileHandle:
                    datasetDirectoryLogs = json.load(fileHandle)
            except:
                pass
            finally:
                datasetDirectoryLogs.append(entry)
                with open(self.fileName, 'w') as fileHandle:
                    json.dump(datasetDirectoryLogs, fileHandle, indent=4)

    def updateListOfDatasets(self):
        finalListOfDatasets = []

        if not os.path.exists(self.fileName):
            return
        else:
            try:
                with open(self.fileName, 'r') as fileHandle:
                    listOfDatasets = json.load(fileHandle)
            except:
                return
            else:
                for entry in listOfDatasets:
                    for name, location in entry.items():
                        for locationKey, directoryPath in location.items():
                            if os.path.exists(directoryPath):
                                finalListOfDatasets.append(entry)

                with open(self.fileName, 'w') as fileHandle:
                    json.dump(finalListOfDatasets, fileHandle, indent=4)

    def getNamesOfDataset(self):
        self.updateListOfDatasets()
        namesOfDatasets = []

        try:
            with open(self.fileName, 'r') as fileHandle:
                listOfDatasets = json.load(fileHandle)
        except:
            return None
        else:
            for entry in listOfDatasets:
                for name, location in entry.items():
                    namesOfDatasets.append(name)

            return namesOfDatasets

    def getBaseDirectoryLocationOfDataset(self, nameOfDataset):
        self.updateListOfDatasets()

        try:
            with open(self.fileName, 'r') as fileHandle:
                listOfDatasets = json.load(fileHandle)
        except:
            # print('kono dataset nai')
            return False, None
        else:
            for entry in listOfDatasets:
                for name, location in entry.items():
                    if name.lower() == nameOfDataset.lower():
                        for locationKey, locationPath in location.items():
                            return True, locationPath

            return False, None

    def isDatasetExist(self, datasetName):
        self.updateListOfDatasets()

        try:
            with open(self.fileName, 'r') as fileHandle:
                listOfDatasets = json.load(fileHandle)
        except:
            return False
        else:
            for entry in listOfDatasets:
                for name, location in entry.items():
                    if name.lower() == datasetName.lower():
                        return True

            return False


if __name__ == '__main__':
    # baseDirectoryName = 'E:/Dataset'
    datasetDirectoryLogs = DatasetDirectoryLogs()
    # datasetDirectoryLogs.addToDatasetDirectoryLogs(baseDirectoryName)
    # datasetDirectoryLogs.updateListOfDatasets()
    # datasetDirectoryLogs.getNamesOfDataset()
    # location = datasetDirectoryLogs.getBaseDirectoryLocationOfDataset('BDSL-50')
    # print(location)
    # location = datasetDirectoryLogs.getBaseDirectoryLocationOfDataset('Sailor')
    # print(location)
    isExist = datasetDirectoryLogs.isDatasetExist('bdsl-50')
    print(isExist)