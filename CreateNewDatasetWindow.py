import os.path

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLineEdit, QLabel, \
    QMainWindow, QFileDialog, QMessageBox

from DatasetDirectoryLogs import DatasetDirectoryLogs


class CreateNewDatasetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Create New Dataset')
        self.setFixedSize(QSize(680, 300))

        self.horizontalLayout = QHBoxLayout()

        self.horizontalLayout2 = QHBoxLayout()

        self.horizontalLayout3 = QHBoxLayout()
        self.horizontalLayout3.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setAlignment(Qt.AlignTop)

        self.centralVerticalLayout = QVBoxLayout()


        self.locationLabel = QLabel('Location:')

        self.datasetLocationLineEdit = QLineEdit()
        self.datasetLocationLineEdit.setPlaceholderText('Specify location for the dataset')
        self.datasetLocationLineEdit.textChanged.connect(self.enableCreateButton)

        self.fileDialogOpeningButton = QPushButton()
        self.fileDialogOpeningButton.setIcon(QIcon('Assets/Icons/folder-medium.png'))

        self.datasetNameLabel = QLabel('Name:')

        self.datasetNameLineEdit = QLineEdit()
        self.datasetNameLineEdit.setPlaceholderText('Specify Name')
        self.datasetNameLineEdit.textChanged.connect(self.enableCreateButton)

        self.backButton = QPushButton('Back')

        self.createButton = QPushButton('Create')
        self.createButton.setEnabled(False)

        self.horizontalLayout.addWidget(self.locationLabel)
        self.horizontalLayout.addWidget(self.datasetLocationLineEdit)
        self.horizontalLayout.addWidget(self.fileDialogOpeningButton)

        self.horizontalLayout2.addWidget(self.datasetNameLabel)
        self.horizontalLayout2.addWidget(self.datasetNameLineEdit)

        self.horizontalLayout3.addWidget(self.backButton)
        self.horizontalLayout3.addWidget(self.createButton)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout2)

        self.centralVerticalLayout.addLayout(self.verticalLayout)
        self.centralVerticalLayout.addLayout(self.horizontalLayout3)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.centralVerticalLayout)

        self.setCentralWidget(self.centralWidget)

        self.fileDialogOpeningButton.clicked.connect(self.openFileDialog)
        # self.createButton.clicked.connect(self.createButtonClicked)


    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = str(QFileDialog.getExistingDirectory(self, "Select Directory", options=options))
        if fileName:
            self.datasetLocationLineEdit.setText(fileName)


    def enableCreateButton(self):
        if len(self.datasetLocationLineEdit.text()) > 0 and len(self.datasetNameLineEdit.text()) > 0:
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

    def createButtonClicked(self):
        datasetDirectoryLogs = DatasetDirectoryLogs()

        isDatasetExist = datasetDirectoryLogs.isDatasetExist(self.datasetNameLineEdit.text())
        # print(isDataseExist)
        isLocationExist = os.path.exists(self.datasetLocationLineEdit.text())

        if not isLocationExist:
            locationFoundDialog = QMessageBox(self)
            locationFoundDialog.setWindowTitle('Location does not exist')
            locationFoundDialog.setText('Please enter a valid location')
            locationFoundDialog.setStandardButtons(QMessageBox.Ok)
            locationFoundDialog.setIcon(QMessageBox.Warning)
            locationFoundDialog.exec()

            self.datasetLocationLineEdit.clear()
            self.enableCreateButton()
            return True

        if isDatasetExist:
            datasetFoundDialog = QMessageBox(self)
            datasetFoundDialog.setWindowTitle('Dataset Found!')
            datasetFoundDialog.setText('There is a dataset of that name. Please Specify another name')
            datasetFoundDialog.setStandardButtons(QMessageBox.Ok)
            datasetFoundDialog.setIcon(QMessageBox.Warning)
            datasetFoundDialog.exec()

            self.datasetNameLineEdit.clear()
            self.enableCreateButton()
            return True
        else:
            return False




if __name__ == '__main__':
    app = QApplication([])
    window = CreateNewDatasetWindow()
    window.show()
    app.exec()