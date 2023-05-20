import cv2
import mediapipe as mp
import numpy as np

class PoseEstimation:
    def __init__(self,
        staticImageMode = False,
        modelComplexity = 1,
        smoothLandmarks = True,
        enableSegmentation = False,
        smoothSegmentation = True,
        refineFaceLandmarks = False,
        minDetectionConfidence = 0.8,
        minTrackingConfidence = 0.7
    ):

        self.staticImageMode = staticImageMode
        self.modelComplexity = modelComplexity
        self.smoothLandmarks = smoothLandmarks
        self.enableSegmentation = enableSegmentation
        self.smoothSegmentation = smoothSegmentation
        self.refineFaceLandmarks = refineFaceLandmarks
        self.minDetectionConfidence = minDetectionConfidence
        self.minTrackingConfidence = minTrackingConfidence


        self.mpHolistic = mp.solutions.holistic
        self.holistic = self.mpHolistic.Holistic(
            self.staticImageMode,
            self.modelComplexity,
            self.smoothLandmarks,
            self.enableSegmentation,
            self.smoothSegmentation,
            self.refineFaceLandmarks,
            self.minDetectionConfidence,
            self.minTrackingConfidence
        )

        self.mpDraw = mp.solutions.drawing_utils

    def processImage(self, image):
        rgbImage = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        rgbImage.flags.writeable = False
        self.results = self.holistic.process(rgbImage)


    def extractFaceLandmarks(self):
        faceLandmarks = []
        if self.results.face_landmarks:
            for faceLandmark in self.results.face_landmarks.landmark:
                faceLandmarks.append([faceLandmark.x, faceLandmark.y, faceLandmark.z])

            faceLandmarks = np.array(faceLandmarks).flatten()
        else:
            faceLandmarks = np.zeros(468 * 3)

        return faceLandmarks

    def extractLeftHandLandmarks(self):
        leftHandLandmarks = []
        if self.results.left_hand_landmarks:
            for leftHandLandmark in self.results.left_hand_landmarks.landmark:
                leftHandLandmarks.append([leftHandLandmark.x, leftHandLandmark.y, leftHandLandmark.z])

            leftHandLandmarks = np.asarray(leftHandLandmarks).flatten()
        else:
            leftHandLandmarks = np.zeros(21 * 3)

        return leftHandLandmarks


    def extractRightHandLandmarks(self):
        rightHandLandmarks = []
        if self.results.right_hand_landmarks:
            for rightHandLandmark in self.results.right_hand_landmarks.landmark:
                rightHandLandmarks.append([rightHandLandmark.x, rightHandLandmark.y, rightHandLandmark.z])

            rightHandLandmarks = np.array(rightHandLandmarks).flatten()
        else:
            rightHandLandmarks = np.zeros(21 * 3)

        return rightHandLandmarks

    def extractPoseLandmarks(self):
        poseLandmarks = []
        if self.results.pose_landmarks:
            for poseLandmark in self.results.pose_landmarks.landmark:
                poseLandmarks.append([poseLandmark.x, poseLandmark.y, poseLandmark.z, poseLandmark.visibility])

            poseLandmarks = np.array(poseLandmarks).flatten()
            # print(len(poseLandmarks))
        else:
            poseLandmarks = np.zeros(132)

        return poseLandmarks

    def drawOverImage(self , image):
        self.mpDraw.draw_landmarks(
            image,
            self.results.pose_landmarks,
            self.mpHolistic.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mpDraw.DrawingSpec(
                color=(80, 110, 10),
                thickness=1,
                circle_radius=1
            ),
            connection_drawing_spec=self.mpDraw.DrawingSpec(
                color=(80, 256, 121),
                thickness=1,
                circle_radius=1
            )
        )

        self.mpDraw.draw_landmarks(
            image,
            self.results.left_hand_landmarks,
            self.mpHolistic.HAND_CONNECTIONS,
            landmark_drawing_spec= self.mpDraw.DrawingSpec(
                color = (80,110,10),
                thickness= 1,
                circle_radius= 1
            ),
            connection_drawing_spec = self.mpDraw.DrawingSpec(
                color=(80, 256, 121),
                thickness=1,
                circle_radius=1
            )
        )
        self.mpDraw.draw_landmarks(
            image,
            self.results.right_hand_landmarks,
            self.mpHolistic.HAND_CONNECTIONS,
            landmark_drawing_spec=self.mpDraw.DrawingSpec(
                color=(80, 110, 10),
                thickness=1,
                circle_radius=1
            ),
            connection_drawing_spec=self.mpDraw.DrawingSpec(
                color=(80, 256, 121),
                thickness=1,
                circle_radius=1
            )
        )
        self.mpDraw.draw_landmarks(
            image,
            self.results.face_landmarks,
            self.mpHolistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=self.mpDraw.DrawingSpec(
                color=(80, 110, 10),
                thickness=1,
                circle_radius=1
            ),
            connection_drawing_spec=self.mpDraw.DrawingSpec(
                color=(80, 256, 121),
                thickness=1,
                circle_radius=1
            )

        )

    def extractKeyPoints(self, image, draw=False):
        self.processImage(image)
        if draw:
            self.drawOverImage(image)

        poseLandmarks = self.extractPoseLandmarks()
        rightHandLandmarks = self.extractRightHandLandmarks()
        leftHandLandmarks = self.extractLeftHandLandmarks()
        faceLandmarks = self.extractFaceLandmarks()

        return np.concatenate([poseLandmarks, faceLandmarks, leftHandLandmarks, rightHandLandmarks])