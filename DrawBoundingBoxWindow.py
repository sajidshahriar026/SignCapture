import os

import cv2
from PyQt5.QtCore import Qt, QSize, QRect, QModelIndex, QThread
from PyQt5.QtGui import QPixmap, QStandardItemModel, QImage, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QListView, QApplication, \
    QWidget, QAbstractItemView
from PyQt5.uic.properties import QtGui

from BoundingBoxWorker import BoundingBoxWorker
from DirectorySetup import DirectorySetup


class DrawBoundingBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Bounding Box')
        self.setFixedSize(QSize(500,500))

        self.horizontalLayout = QHBoxLayout()

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setAlignment(Qt.AlignCenter)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setAlignment(Qt.AlignLeft)

        self.verticalLayout2 = QVBoxLayout()
        self.verticalLayout2.setAlignment(Qt.AlignCenter)

        self.listViewOfImageDirectories = QListView()
        self.listViewOfImageDirectories.setFixedWidth(100)
        self.modelForListViewOfImageDirectories = QStandardItemModel()
        self.listViewOfImageDirectories.setModel(self.modelForListViewOfImageDirectories)
        self.listViewOfImageDirectories.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.openDirectoryButton = QPushButton('Open Directory')

        self.listViewOfImages = QListView()
        self.listViewOfImages.setFixedHeight(350)
        self.listViewOfImages.setFixedWidth(400)
        self.modelForListViewOfImages = QStandardItemModel()
        self.listViewOfImages.setModel(self.modelForListViewOfImages)
        self.listViewOfImages.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.openButton = QPushButton('Open')
        self.openButton.setEnabled(False)

        self.responseMessageLabel = QLabel()
        self.responseMessageLabel.setWordWrap(True)

        self.saveButton = QPushButton('Save')
        self.saveButton.setEnabled(False)

        self.deleteButton = QPushButton('Discard')
        self.deleteButton.setEnabled(False)

        self.horizontalLayout3 = QHBoxLayout()

        self.horizontalLayout3.addWidget(self.saveButton)
        self.horizontalLayout3.addWidget(self.deleteButton)

        self.verticalLayout.addWidget(self.listViewOfImageDirectories)
        self.verticalLayout.addWidget(self.openDirectoryButton)

        self.verticalLayout2.addWidget(self.listViewOfImages)
        self.verticalLayout2.addWidget(self.responseMessageLabel)
        self.verticalLayout2.addWidget(self.openButton)
        self.verticalLayout2.addLayout(self.horizontalLayout3)

        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout2)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralWidget)


        self.openDirectoryButton.clicked.connect(self.openDirectoryButtonClicked)
        self.openButton.clicked.connect(self.openButtonClicked)
        self.saveButton.clicked.connect(self.saveCoordinates)
        self.deleteButton.clicked.connect(self.deleteCoordinates)


    def setBaseDirectoryName(self, baseDirectoryName):
        self.baseDirectoryName = baseDirectoryName

    def updateListViewOfImageDirectories(self):
        directorySetup = DirectorySetup()
        self.imagePath = directorySetup.getImagesPath(self.baseDirectoryName)
        self.imageDirectories = os.listdir(self.imagePath)

        self.modelForListViewOfImageDirectories.clear()
        for dir in self.imageDirectories:
            self.modelForListViewOfImageDirectories.appendRow(QStandardItem(dir))

    def openDirectoryButtonClicked(self):
        try:
            index = self.listViewOfImageDirectories.selectedIndexes()
        except:
            index = None

        if index:
            imageDirectory = self.listViewOfImageDirectories.model().itemData(index[0])
            imageDirectory = imageDirectory[0]
            directorySetup = DirectorySetup()
            imageDirectoryPath = directorySetup.getImagesPath(self.baseDirectoryName)
            imageDirectoryPath = os.path.join(imageDirectoryPath, imageDirectory)
            # print(imageDirectoryPath)

            imagesList = os.listdir(imageDirectoryPath)
            # print(imagesList)

            self.modelForListViewOfImages.clear()
            for image in imagesList:
                self.modelForListViewOfImages.appendRow(QStandardItem(image))

            self.openButton.setEnabled(True)

    def openButtonClicked(self):
        try:
            index = self.listViewOfImages.selectedIndexes()
        except:
            index = None

        if index:
            self.imageName = self.listViewOfImages.model().itemData(index[0])
            self.imageName = self.imageName[0]
            # print(self.imageName)

            self.boundingBoxThread = QThread()
            self.boundingBoxWorker = BoundingBoxWorker()
            self.boundingBoxWorker.moveToThread(self.boundingBoxThread)

            self.boundingBoxThread.started.connect(
                lambda:  self.boundingBoxWorker.drawBoundingBox(self.baseDirectoryName, self.imageName)
            )

            self.boundingBoxWorker.started.connect(self.boundingBoxStarted)

            self.boundingBoxWorker.completion.connect(self.getCoordinates)
            self.boundingBoxWorker.finished.connect(self.boundingBoxThread.quit)
            self.boundingBoxWorker.finished.connect(self.boundingBoxFinished)
            self.boundingBoxWorker.finished.connect(self.boundingBoxWorker.deleteLater)
            self.boundingBoxThread.finished.connect(self.boundingBoxThread.deleteLater)

            self.boundingBoxThread.start()

    def boundingBoxStarted(self):
        self.openButton.setEnabled(False)
        self.openDirectoryButton.setEnabled(False)
        self.responseMessageLabel.setStyleSheet('background-color: lightgreen')
        self.responseMessageLabel.setText(
            'Click and drag LMB to get bounding boxes, click RMB to clear, Q to quit '
        )
    def boundingBoxFinished(self):
        self.saveButton.setEnabled(True)
        self.deleteButton.setEnabled(True)

    def getCoordinates(self, allCoordinates):
        self.allCoordinates  = allCoordinates

    def saveCoordinates(self):
        if len(self.allCoordinates)>0:
            directorySetup = DirectorySetup()
            directorySetup.saveCoordinates(self.baseDirectoryName, self.imageName, self.allCoordinates)

        self.deleteButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.openButton.setEnabled(True)
        self.openDirectoryButton.setEnabled(True)
        self.responseMessageLabel.setText('Bounding Box(es) saved')

    def deleteCoordinates(self):
        self.allCoordinates = []
        self.deleteButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.openButton.setEnabled(True)
        self.openDirectoryButton.setEnabled(True)
        self.responseMessageLabel.setText('Bounding Box(es) Discarded')













if __name__ == '__main__':
    app = QApplication([])
    window = DrawBoundingBoxWindow()
    window.setBaseDirectoryName('F:/BDSL-50')
    window.updateListViewOfImageDirectories()
    window.show()
    app.exec()



