import csv
import os

import cv2
from PyQt5.QtCore import QObject, pyqtSignal

from DirectorySetup import DirectorySetup
from PoseEstimation import PoseEstimation


class ProcessVideoWorker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()

    def processVideo(self, baseDirectoryName, videoName):
        directorySetup = DirectorySetup()
        videoDirectoryPath = directorySetup.getVideoPath(baseDirectoryName)
        imageDirectoryPath = directorySetup.getImagesPath(baseDirectoryName)
        keypointsDirectoryPath = directorySetup.getKeyPointsPath(baseDirectoryName)

        videoLocation = os.path.join(videoDirectoryPath, videoName)
        imageSubDirectoryLocation = os.path.join(imageDirectoryPath, videoName.split('.')[0])
        keypointsLocation = os.path.join(keypointsDirectoryPath, videoName.split('.')[0]+'.csv')

        # print(videoDirectoryPath)
        # print(imageDirectoryPath)
        # print(keypointsDirectoryPath)
        #
        # print(videoLocation)
        # print(imageSubDirectoryLocation)
        # print(keypointsLocation)

        poseEstimation = PoseEstimation()
        count = 0
        videoCapture = cv2.VideoCapture(videoLocation)

        self.started.emit()
        while videoCapture.isOpened():
            success, frame = videoCapture.read()
            keypointdict = {}
            if not success:
                break
            else:
                count += 1
                keypointdict['frame number'] = count
                keypoint = poseEstimation.extractKeyPoints(frame)

                for i, value in enumerate(keypoint):
                    keypointdict[i+1] = value
                # print(keypointdict)
                with open(keypointsLocation,'a', newline= '') as fileHandle:
                    writer = csv.DictWriter(fileHandle, fieldnames= keypointdict.keys())
                    writer.writerow(keypointdict)

                imageFileName = videoName.split('.')[0] + '_' + str(count) + '.jpg'
                imagePath = os.path.join(imageSubDirectoryLocation,  imageFileName)
                cv2.imwrite(imagePath,frame)

        videoCapture.release()
        self.finished.emit()









if __name__ == '__main__':
    processVideoWorker = ProcessVideoWorker()
    processVideoWorker.processVideo('F:/BDSL-50','49.avi')
