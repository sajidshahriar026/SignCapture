from PyQt5.QtWidgets import QApplication

from CreateNewDatasetWindow import CreateNewDatasetWindow
from DirectorySetup import DirectorySetup
from DrawBoundingBoxWindow import DrawBoundingBoxWindow
from ModifyExistingDatasetWindow import ModifyExistingDatasetWindow
from RecordVideoWindow import RecordVideoWindow
from StartingWindow import StartingWindow


class Navigation():
    def __init__(self):
        self.startingWindow = StartingWindow()
        self.isStartingWindowVisible = False

        self.createNewDatasetWindow = CreateNewDatasetWindow()
        self.isCreateNewDatasetWindowVisible = False

        self.modifyExistingDatasetWindow = ModifyExistingDatasetWindow()
        self.isModifyExistingDatasetWindowVisible = False

        self.recordVideoWindow = RecordVideoWindow()
        self.isRecordVideoWindowVisible = False

        self.drawBoundingBoxWindow = DrawBoundingBoxWindow()
        self.isDrawBoundingBoxWindowVisible = False

        #signals for navigation
        self.startingWindow.createNewDatasetButton.clicked.connect(self.changeToCreateNewDatasetWindow)
        self.startingWindow.modifyExistingDatasetButton.clicked.connect(self.changeToModifyExistingDatasetWindow)

        self.createNewDatasetWindow.backButton.clicked.connect(self.goBackToStartinWindowFromCreateNewDatasetWindow)
        self.createNewDatasetWindow.createButton.clicked.connect(self.createButtonClicked)

        self.modifyExistingDatasetWindow.backButton.clicked.connect(self.goBackToStartingWindowFromModifyExistingDataset)
        self.modifyExistingDatasetWindow.modifyButton.clicked.connect(self.modifyButtonClicked)
        self.modifyExistingDatasetWindow.drawBoundingBoxButton.clicked.connect(self.drawBoundingBoxClicked)

        self.startNavigation()

    def startNavigation(self):
        self.isStartingWindowVisible = True
        self.startingWindow.show()

    def changeToCreateNewDatasetWindow(self):
        self.isStartingWindowVisible = False
        self.startingWindow.hide()

        self.isCreateNewDatasetWindowVisible = True
        self.createNewDatasetWindow.show()

    def changeToModifyExistingDatasetWindow(self):
        self.isStartingWindowVisible = False
        self.startingWindow.hide()

        self.isModifyExistingDatasetWindowVisible = True
        self.modifyExistingDatasetWindow.updateListViewOfDataset()
        self.modifyExistingDatasetWindow.show()



    def goBackToStartinWindowFromCreateNewDatasetWindow(self):
        self.isCreateNewDatasetWindowVisible = False
        self.createNewDatasetWindow.hide()

        self.isStartingWindowVisible = True
        self.startingWindow.show()

    def goBackToStartingWindowFromModifyExistingDataset(self):
        self.isModifyExistingDatasetWindowVisible = False
        self.modifyExistingDatasetWindow.hide()

        self.isStartingWindowVisible = True
        self.startingWindow.show()


    def createButtonClicked(self):
        isExist = self.createNewDatasetWindow.createButtonClicked()

        if not isExist:
            datasetLocation = self.createNewDatasetWindow.datasetLocationLineEdit.text()
            datasetName = self.createNewDatasetWindow.datasetNameLineEdit.text()

            directorySetup = DirectorySetup()
            self.baseDirectoryName = directorySetup.setUpDirectoriesForNewDatabase(datasetLocation, datasetName)


            self.isCreateNewDatasetWindowVisible = False
            self.createNewDatasetWindow.hide()

            self.isRecordVideoWindowVisible = True
            self.recordVideoWindow.setBaseDirectoryName(self.baseDirectoryName)
            self.recordVideoWindow.updateTreeWidgetOfFiles()
            self.recordVideoWindow.show()




    def modifyButtonClicked(self):
        locationPath = self.modifyExistingDatasetWindow.modifyButtonClicked()


        if locationPath:
            self.baseDirectoryName = locationPath
            self.isModifyExistingDatasetWindowVisible = False
            self.modifyExistingDatasetWindow.hide()

            self.isRecordVideoWindowVisible = True
            self.recordVideoWindow.setBaseDirectoryName(self.baseDirectoryName)
            self.recordVideoWindow.updateTreeWidgetOfFiles()
            self.recordVideoWindow.show()

    def drawBoundingBoxClicked(self):
        locationPath = self.modifyExistingDatasetWindow.modifyButtonClicked()
        if locationPath:
            self.baseDirectoryName = locationPath
            self.isModifyExistingDatasetWindowVisible = False
            self.modifyExistingDatasetWindow.hide()

            self.isDrawBoundingBoxWindowVisible = True
            self.drawBoundingBoxWindow.setBaseDirectoryName(self.baseDirectoryName)
            self.drawBoundingBoxWindow.updateListViewOfImageDirectories()
            self.drawBoundingBoxWindow.show()

if __name__ == '__main__':
    app = QApplication([])
    navigation = Navigation()
    app.exec()