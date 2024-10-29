# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 00:02:36 2023

@author: Ali
"""

import cv2
import mediapipe as mp
import glob
import matplotlib.pyplot as plt
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
path = "test-img/*.jpg"

detected = 0


with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    for file in glob.glob(path):
        print(file)
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(image)
        annotated_image = image.copy()

        detected = detected + len(results.detections)

        # Draw face detections of each face.
        if results.detections:
            for detection in results.detections:
                print('Nose tip:')
                print(mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))

                mp_drawing.draw_detection(annotated_image, detection)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                font_color = (0, 255, 0)  # BGR color format
                font_thickness = 1
                cv2.putText(annotated_image, "Detected Faces:", (50, 60), font, font_scale,
                            font_color, font_thickness, cv2.LINE_AA)

                cv2.putText(annotated_image, str(len(results.detections)), (50, 100), font, font_scale,
                            font_color, font_thickness, cv2.LINE_AA)
                right_eye = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE)
                left_eye = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.LEFT_EYE)

        plt.figure()
        plt.imshow(annotated_image)
        plt.show()

print("Number of detected faces", detected)
