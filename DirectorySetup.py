import json
import os
import csv

from DatasetDirectoryLogs import DatasetDirectoryLogs


class DirectorySetup():
    def setUpDirectoriesForNewDatabase(self, datasetLocation, datasetName):
        self.datasetLocation = datasetLocation
        self.datasetName = datasetName

        self.baseDirectoryName = os.path.join(self.datasetLocation, self.datasetName)
        os.mkdir(self.baseDirectoryName)

        self.videoPath = 'Videos'
        self.imagePath = 'Images'
        self.keypointsPath = 'Keypoints'
        self.metaInfoPath = 'Meta Information'
        self.jsonFileName = self.datasetName + '.json'
        # print(self.baseDirectoryName)
        # print(self.jsonFileName)

        self.videoPath = os.path.join(self.baseDirectoryName, self.videoPath)
        self.imagePath = os.path.join(self.baseDirectoryName, self.imagePath)
        self.keypointsPath = os.path.join(self.baseDirectoryName, self.keypointsPath)
        self.metaInfoPath = os.path.join(self.baseDirectoryName, self.metaInfoPath)
        self.jsonFileName = os.path.join(self.baseDirectoryName, self.jsonFileName)
        # print(self.jsonFileName)

        if not os.path.exists(self.videoPath):
            os.mkdir(self.videoPath)
        if not os.path.exists(self.imagePath):
            os.mkdir(self.imagePath)
        if not os.path.exists(self.keypointsPath):
            os.mkdir(self.keypointsPath)
        if not os.path.exists(self.metaInfoPath):
            os.mkdir(self.metaInfoPath)

        if not os.path.exists(self.jsonFileName):
            file = open(self.jsonFileName,'x')
            file.close()

        datasetDirectoryLogs = DatasetDirectoryLogs()
        datasetDirectoryLogs.addToDatasetDirectoryLogs(self.baseDirectoryName)

        return self.baseDirectoryName

    def getBaseDirectoryDetails(self, baseDirectoryName):
        self.baseDirectoryName = baseDirectoryName

        self.baseDirectoryDetails = {}

        for subDirectoryName in os.listdir(self.baseDirectoryName):
            subDirectoryPath = os.path.join(self.baseDirectoryName,subDirectoryName)
            # print(subDirectoryPath)
            self.baseDirectoryDetails[subDirectoryName] = []
            # print(self.baseDirectoryDetails)
            if os.path.isdir(subDirectoryPath):
                for subSubDirectoryName in os.listdir(subDirectoryPath):
                    self.baseDirectoryDetails[subDirectoryName].append(subSubDirectoryName)


        # print(self.baseDirectoryDetails)
        return self.baseDirectoryDetails


    def getVideoPath(self, baseDirectoryName):
        # print(os.path.join(baseDirectoryName, 'Videos'))
        return os.path.join(baseDirectoryName, 'Videos')

    def getImagesPath(self, baseDirectoryName):
        # print(os.path.join(baseDirectoryName, 'Images'))
        return os.path.join(baseDirectoryName, 'Images')

    def getKeyPointsPath(self, baseDirectoryName):
        # print(os.path.join(baseDirectoryName, 'Images'))
        return os.path.join(baseDirectoryName, 'Keypoints')

    def getMetaInformationPath(self, baseDirectoryName):
        # print(os.path.join(baseDirectoryName, 'Images'))
        return os.path.join(baseDirectoryName, 'Meta Information')

    def getJSONFilePath(self, baseDirectoryName):
        dirs = os.listdir(baseDirectoryName)

        for dir in dirs:
            if not os.path.isdir(os.path.join(baseDirectoryName, dir)):
                _, extension = os.path.splitext(os.path.join(baseDirectoryName, dir))
                if extension =='.json':
                    # print(os.path.join(baseDirectoryName, dir))
                    return os.path.join(baseDirectoryName, dir)



    def appendToJsonFile(self, baseDirectoryName, entry):
        jsonFileLogs = []
        # entry = {'hello': 'bye'}
        jsonFilePath = self.getJSONFilePath(baseDirectoryName)
        try:
            with open(jsonFilePath, 'r', encoding='utf-8') as fileHandle:
                jsonFileLogs = json.load(fileHandle)

        except:
            pass
        finally:
            # print(jsonFileLogs)
            jsonFileLogs.append(entry)
            with open(jsonFilePath, 'w', encoding='utf-8') as fileHandle:
                json.dump(jsonFileLogs,fileHandle, indent = 4)




    def createImageFolder(self, baseDirectoryName, videoName):
        imagesFolderPath = self.getImagesPath(baseDirectoryName)
        imagesFolderName = videoName.split('.')[0]
        imagesFolderPath = os.path.join(imagesFolderPath, imagesFolderName)
        if not os.path.exists(imagesFolderPath):
            os.mkdir(imagesFolderPath)

    def createKeyPointsCSV(self, baseDirectoryName, videoName):
        keypointsFolderPath = self.getKeyPointsPath(baseDirectoryName)
        csvFileName = videoName.split('.')[0] + '.csv'
        keypointsFolderPath = os.path.join(keypointsFolderPath, csvFileName)

        headerList = ['frame number']
        for i in range(1, 1663):
            headerList.append(i)

        if not os.path.exists(keypointsFolderPath):
            with open(keypointsFolderPath,'w') as fileHandle:
                dictWriter = csv.DictWriter(fileHandle, delimiter = ',' ,fieldnames= headerList)

                dictWriter.writeheader()

        # print(headerList)


    def createMetaInfoJSON(self,baseDirectoryName, videoName):
        metaInfoFolderPath = self.getMetaInformationPath(baseDirectoryName)
        jsonFileName = videoName.split('.')[0] + '.json'
        metaInfoFolderPath = os.path.join(metaInfoFolderPath, jsonFileName)
        if not os.path.exists(metaInfoFolderPath):
            file = open(metaInfoFolderPath,'x')
            file.close()


    def saveVideo(self, baseDirectoryName,videoName, size, duration, gestureName):
        videoLocation = os.path.join(self.getVideoPath(baseDirectoryName), videoName)


        self.entry = {
            videoName:{
                'location':  videoLocation,
                'dimension': size,
                'duration' : duration,
                'gestureName': gestureName,
            }
        }

        self.appendToJsonFile(baseDirectoryName, self.entry)
        self.createImageFolder(baseDirectoryName, videoName)
        self.createKeyPointsCSV(baseDirectoryName, videoName)
        self.createMetaInfoJSON(baseDirectoryName, videoName)


    def deleteVideo(self, baseDirectoryName, videoName):
        videoLocation = os.path.join(self.getVideoPath(baseDirectoryName), videoName)

        # print(videoLocation)
        if os.path.exists(videoLocation):
            os.remove(videoLocation)

    def saveCoordinates(self, baseDirectoryName, imageName, allCoordinates):
        metaInfoPath = self.getMetaInformationPath(baseDirectoryName)
        print(metaInfoPath)
        metaInfoPathFileName = imageName.split('_')[0] + '.json'
        print(metaInfoPathFileName)

        metaInfoFilePath = os.path.join(metaInfoPath, metaInfoPathFileName)
        print(metaInfoFilePath)
        entry = {imageName: allCoordinates}
        print(entry)
        metaInfoLogs = []
        try:
            with open(metaInfoFilePath, 'r') as fileHandle:
                metaInfoLogs = json.load(fileHandle)
        except:
            pass
        finally:
            metaInfoLogs.append(entry)
            with open(metaInfoFilePath, 'w') as fileHandle:
                json.dump(metaInfoLogs, fileHandle, indent = 4)







if __name__ == '__main__':
     directorySetup = DirectorySetup()
     # directorySetup.setUpDirectoriesForNewDatabase('E:/Dataset')
     # directorySetup.getBaseDirectoryDetails('F:/BDSL-50')
     # directorySetup.getVideoPath('F:/BDSL-50')
     # directorySetup.saveVideo('F:/BDSL-50','1.avi',1,2,3)
     # directorySetup.getJSONFilePath('F:/BDSL-50')
     # directorySetup.appendToJsonFile('F:/BDSL-50')
     # directorySetup.deleteVideo('F:/BDSL-50', '47.avi')
     # directorySetup.createKeyPointsCSV('F:/BDSL-50', '47.avi')
     directorySetup.saveCoordinates('F:/dummy', '1_2.jpg', [[1,2], [2,3]])