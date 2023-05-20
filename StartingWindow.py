from PyQt5.QtCore import QSize,Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QWidget, QMainWindow

from CreateNewDatasetWindow import CreateNewDatasetWindow


class StartingWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(400,300))
        self.setWindowTitle('Sign Capture')

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.createNewDatasetButton = QPushButton('Create New Dataset')
        self.modifyExistingDatasetButton = QPushButton('Modify Existing Dataset')

        self.layout.addWidget(self.createNewDatasetButton)
        self.layout.addWidget(self.modifyExistingDatasetButton)

        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.layout)

        self.setCentralWidget(self.centralWidget)


if __name__ == '__main__':
    app = QApplication([])
    window = StartingWindow()
    window.show()
    app.exec()