import cv2
import mediapipe as mp
import os
import numpy as np
import math
import matplotlib as plt
from matplotlib import pyplot as plt


path = 'images/'


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
image_files = os.listdir(path)


def vect(Q):
    return 0.5 * np.array([[Q[2][1]-Q[1][2]],
                           [Q[0][2]-Q[2][0]],
                           [Q[1][0]-Q[0][1]]])


def trace(Q):
    return (Q[0][0] + Q[1][1] + Q[2][2])


def skew(x):
    return np.array([[0, -x[2][0], x[1][0]],
                     [x[2][0], 0, -x[0][0]],
                     [-x[1][0], x[0][0], 0]])


def rotation_matrix(image1, image2):

    e1 = (image1[1] - image1[0]).transpose()
    e2 = (image1[2] - image1[0]).transpose()
    e3 = (image1[3] - image1[0]).transpose()
    e1_ = image2[1] - image2[0]
    e2_ = image2[2] - image2[0]
    e3_ = image2[3] - image2[0]
    Q = np.array([[np.dot(e1, e1_), np.dot(e1, e2_), np.dot(e1, e3_)], [np.dot(e2, e1_), np.dot(
        e2, e2_), np.dot(e2, e3_)], [np.dot(e3, e1_), np.dot(e3, e2_), np.dot(e3, e3_)]])

    Q = np.reshape(Q, (3, 3))
    det = np.linalg.det(Q)

    return Q, det


def rotation_angle(trace):
    rotation_angle = math.acos((trace-1)/2)
    return rotation_angle * (180/math.pi)


def rotation_axis(vect, angle):
    e = vect/math.sin(angle)
    return e


def pluker(image1, image2, Q, angle, rotation_axis):
    # using elbow as rotated points
    point1 = image1[1]
    point1_transformed = image2[1]

    p0 = np.dot(((Q-np.identity(3)).transpose()),
                (np.dot(Q, point1) - point1_transformed)) / 2*(1-math.cos(angle))

    moment = np.cross(p0, rotation_axis, axis=0)

    pluker = np.concatenate((p0, moment))
    return pluker


landmark = []
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

    for image_file in image_files:
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.

        image = cv2.imread(os.path.join(path, image_file))
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

        shoulder = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        shoulder_vect = np.array([[shoulder.x], [shoulder.y], [shoulder.z]])

        elbow = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        elbow_vect = np.array([[elbow.x], [elbow.y], [elbow.z]])

        wrist = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        wrist_vect = np.array([[wrist.x], [wrist.y], [wrist.z]])

        index = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX]
        index_vect = np.array([[index.x], [index.y], [index.z]])

        if image_file == image_files[1]:
            image1 = [shoulder_vect, elbow_vect, wrist_vect, index_vect]
        else:
            image2 = [shoulder_vect, elbow_vect, wrist_vect, index_vect]

        landmark.append(image)


Q, det = rotation_matrix(image1, image2)


angle = rotation_angle(trace(Q))

rotation_ax = rotation_axis(vect(Q), angle)

pluker_line = pluker(image1, image2, Q, angle, rotation_ax)

Q_new = ((1/det)**(1/3))*Q
print(Q_new)


landmark1 = landmark[0]
landmark2 = landmark[1]
Hori = np.concatenate((landmark1, landmark2), axis=1)


font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.7
font_color = (0, 0, 0)  # BGR color format
font_thickness = 1


y1 = 60
cv2.putText(Hori, "rotation matrix is:", (600, 30), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)
for i in range(len(Q)):
    Q_string = (np.array2string(Q[i]))

    cv2.putText(Hori, Q_string, (600, y1), font, font_scale,
                font_color, font_thickness, cv2.LINE_AA)
    y1 = y1+30


rotation_axis_string = np.array2string(rotation_ax.transpose())
cv2.putText(Hori, "rotation axis is:", (50, 30), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)

cv2.putText(Hori, rotation_axis_string, (50, 60), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)


cv2.putText(Hori, "rotation angle is:", (600, 200), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)

cv2.putText(Hori, str(angle), (700, 230), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)


pluker_line_reshape = np.reshape(pluker_line, (2, 3))

pluker_string2 = np.array2string(pluker_line_reshape[1])

cv2.putText(Hori, "pluker line is(6*1 vector):", (1300, 30), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)

cv2.putText(Hori, "first three elements", (1300, 60), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)
cv2.putText(Hori, "second three elements", (1300, 120), font, font_scale,
            font_color, font_thickness, cv2.LINE_AA)
y2 = 60
for i in range(len(pluker_line_reshape)):
    pluker_string = np.array2string(pluker_line_reshape[i])

    cv2.putText(Hori, pluker_string, (1300, y2+30), font, font_scale,
                font_color, font_thickness, cv2.LINE_AA)
    y2 = y2+60

cv2.imshow('result', Hori)
cv2.waitKey(0)
