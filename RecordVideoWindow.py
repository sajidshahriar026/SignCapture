import logging

from PyQt5.QtCore import QSize, Qt, QThread

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit, \
    QLabel, QTreeWidget, QTreeWidgetItem

from DirectorySetup import DirectorySetup
from ProcessVideoWorker import ProcessVideoWorker
from RecordVideoWorker import RecordVideoWorker


logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt = '%H:%M:%S')


class RecordVideoWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Record')
        self.setFixedSize(QSize(600,600))

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout3 = QHBoxLayout()
        self.horizontalLayout3.setAlignment(Qt.AlignLeft)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setAlignment(Qt.AlignLeft|Qt.AlignCenter|Qt.AlignTop)

        self.verticalLayout2 = QVBoxLayout()
        self.verticalLayout2.setAlignment(Qt.AlignLeft | Qt.AlignCenter)

        self.verticalLayout3 = QVBoxLayout()
        self.verticalLayout3.setAlignment(Qt. AlignBottom)

        self.treeWidgetOfFiles = QTreeWidget()
        self.treeWidgetOfFiles.setFixedWidth(300)

        self.startRecordingButton = QPushButton('Start Recording')
        self.startRecordingButton.setFixedSize(QSize(100,40))

        self.gestureNameLineEdit = QLineEdit()
        self.gestureNameLineEdit.setStyleSheet("font-size: 15px")
        self.gestureNameLineEdit.setPlaceholderText('Specify Gesture Label')
        self.gestureNameLineEdit.setEnabled(False)

        self.saveButton = QPushButton('Save')
        self.saveButton.setEnabled(False)

        self.discardButton = QPushButton('Discard')
        self.discardButton.setEnabled(False)

        self.processVideoButton = QPushButton('Process Video Button')
        self.processVideoButton.setEnabled(False)

        self.responseMessageLabel = QLabel()
        self.responseMessageLabel.setStyleSheet('font-size: 20px')
        self.responseMessageLabel.setWordWrap(True)

        self.horizontalLayout2.addWidget(self.startRecordingButton)

        self.horizontalLayout3.addWidget(self.saveButton)
        self.horizontalLayout3.addWidget(self.discardButton)

        self.verticalLayout2.addLayout(self.horizontalLayout2)
        self.verticalLayout2.addWidget(self.gestureNameLineEdit)
        self.verticalLayout2.addLayout(self.horizontalLayout3)
        self.verticalLayout2.addWidget(self.processVideoButton)
        self.verticalLayout2.addWidget(self.responseMessageLabel)

        self.horizontalLayout.addWidget(self.treeWidgetOfFiles)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout2)

        self.widget = QWidget()
        self.widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(self.widget)

        self.startRecordingButton.clicked.connect(self.startRecordVideoWorker)
        self.gestureNameLineEdit.textChanged.connect(self.gestureNameLineEditTextChanged)
        self.saveButton.clicked.connect(self.saveButtonClicked)
        self.discardButton.clicked.connect(self.discardButtonClicked)
        self.processVideoButton.clicked.connect(self.processVideoButtonClicked)

    def setBaseDirectoryName(self,baseDirectoryName):
        self.baseDirectoryName = baseDirectoryName

    def updateTreeWidgetOfFiles(self):
        directorySetup = DirectorySetup()
        self.baseDirectoryDetails = directorySetup.getBaseDirectoryDetails(self.baseDirectoryName)

        self.treeWidgetOfFiles.setHeaderLabel(self.baseDirectoryName.split('/')[-1])

        self.treeItems = []

        for subDirectory, subDirectoryList in self.baseDirectoryDetails.items():
            subDirectoryNode = QTreeWidgetItem([subDirectory])
            for subSubDirectory in subDirectoryList:
                subSubDirectoryNode = QTreeWidgetItem([subSubDirectory])

                subDirectoryNode.addChild(subSubDirectoryNode)

            self.treeItems.append(subDirectoryNode)

        self.treeWidgetOfFiles.insertTopLevelItems(0,self.treeItems)

    def startRecordVideoWorker(self):
        self.recordVideoThread = QThread()

        self.recordVideoWorker = RecordVideoWorker()

        self.recordVideoWorker.moveToThread(self.recordVideoThread)

        self.recordVideoThread.started.connect(
            lambda: self.recordVideoWorker.recordVideo(self.baseDirectoryName)
        )

        self.recordVideoWorker.started.connect(
            lambda: self.recordingStarted()
        )
        self.recordVideoWorker.completion.connect(self.currentVideoDetails)
        self.recordVideoWorker.finished.connect(self.recordVideoThread.quit)
        self.recordVideoWorker.finished.connect(self.recordingFinished)
        self.recordVideoWorker.finished.connect(self.recordVideoWorker.deleteLater)
        self.recordVideoThread.finished.connect(self.recordVideoThread.deleteLater)

        self.recordVideoThread.start()

    def recordingStarted(self):
        self.startRecordingButton.setEnabled(False)
        self.responseMessageLabel.setText('Recording Started. Press Q to stop recording')
        self.responseMessageLabel.setStyleSheet('background-color: lightgreen; font-size: 20px')

    def currentVideoDetails(self, videoDetails):
        self.currentVideoName, self.curentVideoSize, self.currentVideoDuration = videoDetails

        # print(self.currentVideoName)
        # print(self.size)
        # print(self.duration)

    def recordingFinished(self):
        self.gestureNameLineEdit.setEnabled(True)
        self.discardButton.setEnabled(True)

        self.responseMessageLabel.setText('Recording Finished')

    def gestureNameLineEditTextChanged(self, text):
        if len(self.gestureNameLineEdit.text()) > 0:
            self.saveButton.setEnabled(True)
        else:
            self.saveButton.setEnabled(False)

    def saveButtonClicked(self):
        gestureName = self.gestureNameLineEdit.text()

        self.discardButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.gestureNameLineEdit.clear()
        self.gestureNameLineEdit.setEnabled(False)

        directorySetup = DirectorySetup()
        directorySetup.saveVideo(self.baseDirectoryName, self.currentVideoName, self.curentVideoSize, self.currentVideoDuration, gestureName)

        self.responseMessageLabel.setText('Video Saved')
        self.processVideoButton.setEnabled(True)

    def discardButtonClicked(self):
        self.saveButton.setEnabled(False)
        self.discardButton.setEnabled(False)
        self.gestureNameLineEdit.setEnabled(False)
        self.gestureNameLineEdit.clear()

        directorySetup = DirectorySetup()
        directorySetup.deleteVideo(self.baseDirectoryName, self.currentVideoName)

        self.responseMessageLabel.setText('Video Discarded')
        self.startRecordingButton.setEnabled(True)

    def processVideoButtonClicked(self):
        self.processVideoButton.setEnabled(False)

        self.processVideoThread = QThread()

        self.processVideoWorker = ProcessVideoWorker()

        self.processVideoWorker.moveToThread(self.processVideoThread)

        self.processVideoThread.started.connect(
            lambda: self.processVideoWorker.processVideo(self.baseDirectoryName, self.currentVideoName)
        )

        self.processVideoWorker.started.connect(self.processingStarted)
        self.processVideoWorker.finished.connect(self.processVideoThread.quit)
        self.processVideoWorker.finished.connect(self.processingFinished)
        self.processVideoWorker.finished.connect(self.processVideoWorker.deleteLater)
        self.processVideoThread.finished.connect(self.recordVideoWorker.deleteLater)

        self.processVideoThread.start()

    def processingStarted(self):
        self.responseMessageLabel.setText('Processing Started')

    def processingFinished(self):
        self.startRecordingButton.setEnabled(True)
        self.responseMessageLabel.setText('Processing Finished')

if __name__ == '__main__':
    app = QApplication([])
    window = RecordVideoWindow()
    window.setBaseDirectoryName('F:/BDSL-50')
    window.updateTreeWidgetOfFiles()
    window.show()
    app.exec()