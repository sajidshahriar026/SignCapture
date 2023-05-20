import os

import cv2
from PyQt5.QtCore import QObject, pyqtSignal

from BoundingBox import BoundingBox
from DirectorySetup import DirectorySetup


class BoundingBoxWorker(QObject):
    finished = pyqtSignal()
    started = pyqtSignal()
    completion = pyqtSignal(list)

    def drawBoundingBox(self, baseDirectoryName,imageName):
        directorySetup = DirectorySetup()
        imageDirectoryPath = directorySetup.getImagesPath(baseDirectoryName)
        imageDirectoryName = imageName.split('_')[0]
        imageDirectoryPath = os.path.join(imageDirectoryPath, imageDirectoryName)

        #
        imagePath = os.path.join(imageDirectoryPath, imageName)
        # print(imagePath)
        self.started.emit()
        boundingBox = BoundingBox(imagePath)
        while True:
            cv2.imshow('image',boundingBox.show_image())
            key = cv2.waitKey(1)

            if key == ord('q'):

                allCoordinates = boundingBox.getAllCoordinates()
                self.completion.emit(allCoordinates)
                break
        cv2.destroyAllWindows()
        self.finished.emit()







if __name__ == '__main__':
    boundingBoxWorker = BoundingBoxWorker()
    boundingBoxWorker.drawBoundingBox('F:/dummy', '1_1.jpg')