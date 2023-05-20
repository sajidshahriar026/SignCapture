import logging
import os
import time

from PyQt5.QtCore import pyqtSignal, Qt, QObject
from PyQt5.QtGui import QImage

import cv2

from DirectorySetup import DirectorySetup

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt = '%H:%M:%S')

class RecordVideoWorker(QObject):
    started = pyqtSignal()
    finished = pyqtSignal()
    completion = pyqtSignal(tuple)

    def recordVideo(self, baseDirectoryName):
        directorySetup = DirectorySetup()
        videoDirectoryPath = directorySetup.getVideoPath(baseDirectoryName)

        listOfVideos = os.listdir(videoDirectoryPath)
        if len(listOfVideos)>0:
            lastVideoName = listOfVideos[-1].split('.')[0]
            lastVideoName = int(lastVideoName)
            videoName = str(lastVideoName + 1) + '.avi'
        else:
            videoName = '1.avi'
        # print(videoName)

        self.videoCapture = cv2.VideoCapture(0)

        if self.videoCapture.isOpened():
            frameWidth = int(self.videoCapture.get(3))
            frameHeight = int(self.videoCapture.get(4))
            size = (frameWidth, frameHeight)

            videoSavePath = os.path.join(videoDirectoryPath, videoName)
            # print(videoSavePath)
            videoFile = cv2.VideoWriter(videoSavePath, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, size)

        self.started.emit()
        startTime = time.time()
        while self.videoCapture.isOpened():
            ret, frame = self.videoCapture.read()
            if ret:
                # flip the image
                frame = cv2.flip(frame, 1)
                videoFile.write(frame)
                cv2.imshow('Frame', frame)

                key = cv2.waitKey(10)

                if key == ord('q'):
                    finishTime = time.time()
                    break

            else:
                finishTime = time.time()
                break

        duration = finishTime - startTime
        self.videoCapture.release()
        cv2.destroyAllWindows()
        videoDetails = (videoName, size, duration)
        self.completion.emit(videoDetails)
        self.finished.emit()

if __name__ == '__main__':
    recordVideoWorker = RecordVideoWorker()
    recordVideoWorker.recordVideo('F:/lol')



