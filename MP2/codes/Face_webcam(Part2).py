# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 00:02:36 2023

@author: Ali
"""

import cv2
import mediapipe as mp
import glob
import matplotlib.pyplot as plt
import numpy as np
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


# For static images:


detected = 0

cap = cv2.VideoCapture(0)
with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)


# Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Convert the BGR image to RGB and process it with MediaPipe Face Detection.

    # Draw face detections of each face.
        if results.detections:
            for detection in results.detections:
                #print('Nose tip:')
                # print(mp_face_detection.get_key_point(
                #   detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
                # mp_drawing.draw_detection(image, detection)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                font_color = (0, 0, 255)  # BGR color format
                font_thickness = 1
                # cv2.imshow('MediaPipe Pose', cv2.flip(cv2.flip(image, 1), 1))
                cv2.putText(image, "Detected Faces:", (100, 60), font, font_scale,
                            font_color, font_thickness, cv2.LINE_AA)

                cv2.putText(image, str(len(results.detections)), (100, 100), font, font_scale,
                            font_color, font_thickness, cv2.LINE_AA)

                # print(len(results.detections))

                right_eye = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE)
                left_eye = mp_face_detection.get_key_point(
                    detection, mp_face_detection.FaceKeyPoint.LEFT_EYE)

                h, w, c = image.shape

                startpoint = (right_eye.x, right_eye.y)
                endpoint = (left_eye.x, left_eye.y)
                thickness = -1
                color = (0, 0, 0)

                image = cv2.rectangle(image, (int(startpoint[0]*w)-40, int(startpoint[1]*h)-10), (int(
                    endpoint[0]*w)+40, int(endpoint[1]*h)+10), color, thickness)
                cv2.imshow('Line', cv2.flip(cv2.flip(image, 1), 1))

                
                if cv2.waitKey(5) & 0xFF == 27:
                    break

cap.release()
cv2. destroyAllWindows()
