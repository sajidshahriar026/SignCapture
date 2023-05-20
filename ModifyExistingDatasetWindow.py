from PyQt5.QtCore import QSize, Qt, QLine
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit, \
    QLabel, QFrame, QListView, QMessageBox, QAbstractItemView

from DatasetDirectoryLogs import DatasetDirectoryLogs


class ModifyExistingDatasetWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Modify')
        self.setFixedSize(QSize(680,540))

        self.verticalLayout = QVBoxLayout()

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.searchDatasetInput = QLineEdit()
        self.searchDatasetInput.setPlaceholderText('Search Dataset')
        self.searchDatasetInput.textChanged.connect(self.searchButtonClicked)

        self.searchButton = QPushButton()
        self.setIconSize(QSize(16,16))
        self.searchButton.setIcon(QIcon('Assets/Icons/search.png'))
        self.searchButton.clicked.connect(self.searchButtonClicked)

        self.horizontalLayout.addWidget(self.searchDatasetInput)
        self.horizontalLayout.addWidget(self.searchButton)

        self.backButton = QPushButton('Back')

        self.modifyButton = QPushButton('Modify')

        self.drawBoundingBoxButton = QPushButton('Draw Bounding Box')
        # self.modifyButton.clicked.connect(self.modifyButtonClicked)

        self.horizontalLayout2.addWidget(self.drawBoundingBoxButton)
        self.horizontalLayout2.addWidget(self.backButton)
        self.horizontalLayout2.addWidget(self.modifyButton)


        self.listViewOfDataset = QListView()
        self.modelForListViewOfDataSet = QStandardItemModel()
        self.listViewOfDataset.setModel(self.modelForListViewOfDataSet)
        self.listViewOfDataset.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addWidget(self.listViewOfDataset)
        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.widget = QWidget()
        self.widget.setLayout(self.verticalLayout)
        self.setCentralWidget(self.widget)

    def updateListViewOfDataset(self):
        datasetDirectoryLogs = DatasetDirectoryLogs()
        self.namesOfDatasets = datasetDirectoryLogs.getNamesOfDataset()

        self.modelForListViewOfDataSet.clear()
        for i in self.namesOfDatasets:
            self.modelForListViewOfDataSet.appendRow(QStandardItem(i))

    def searchButtonClicked(self):
        searchString = self.searchDatasetInput.text()


        if len(searchString)>0:
            self.modelForListViewOfDataSet.clear()
            for name in self.namesOfDatasets:
                if name.lower().startswith(searchString.lower()):
                    self.modelForListViewOfDataSet.appendRow(QStandardItem(name))
        else:
            self.updateListViewOfDataset()

    def modifyButtonClicked(self):
        try:
            index = self.listViewOfDataset.selectedIndexes()
        except:
            index = None
        # print(index)
        if index:
            # print(index)
            nameOfDataset = self.listViewOfDataset.model().itemData(index[0])
            nameOfDataset = nameOfDataset[0]
            # print(nameOfDataset)
            datasetDirectoryLogs = DatasetDirectoryLogs()
            isExist, locationPath = datasetDirectoryLogs.getBaseDirectoryLocationOfDataset(nameOfDataset)
            # print(isExist)

            if not isExist:
                datasetNotExistDialog = QMessageBox(self)
                datasetNotExistDialog.setWindowTitle('Error')
                datasetNotExistDialog.setText('This Dataset Directory may have been removed or replaced')
                datasetNotExistDialog.setStandardButtons(QMessageBox.Ok)
                datasetNotExistDialog.setIcon(QMessageBox.Warning)
                datasetNotExistDialog.exec()

                self.updateListViewOfDataset()

            else:
                return locationPath

        else:
            indexNotSelectedDialog = QMessageBox(self)
            indexNotSelectedDialog.setWindowTitle('Error')
            indexNotSelectedDialog.setText('Please Select a Dataset')
            indexNotSelectedDialog.setStandardButtons(QMessageBox.Ok)
            indexNotSelectedDialog.setIcon(QMessageBox.Warning)
            indexNotSelectedDialog.exec()

            return None




if __name__ == '__main__':
    app = QApplication([])
    window = ModifyExistingDatasetWindow()
    window.updateListViewOfDataset()
    window.show()
    app.exec()
