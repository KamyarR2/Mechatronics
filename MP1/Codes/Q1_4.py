import time
import serial
import numpy as np
import math
import matplotlib.pyplot as plt


arduinoData = serial.Serial('com9', 115200)
time.sleep(1)

toRad = np.pi/180.0
toDeg = 1/toRad


def skew(x):
    return np.array([[0, -x[2][0], x[1][0]],
                     [x[2][0], 0, -x[0][0]],
                     [-x[1][0], x[0][0], 0]])


def natural_parameters(r0, r1, r2, r3):
    phi = 2*math.acos(r0)
    e = np.array([[r1], [r2], [r3]])/math.sin(phi/2)
    return e, phi


def linear_invs(e, phi):
    q0_ = math.cos(phi)
    q = e * math.sin(phi)
    return q, q0_



while True:
    while arduinoData.inWaiting() == 0:
        pass
    dataPacket = arduinoData.readline()
    try:
        dataPacket = str(dataPacket, 'utf-8')
        splitPacket = dataPacket.split(",")
        r0 = float(splitPacket[0])
        r1 = float(splitPacket[1])
        r2 = float(splitPacket[2])
        r3 = float(splitPacket[3])
        # print(r0, r1, r2, r3)
        e, phi = natural_parameters(r0, r1, r2, r3)
        q, q0_ = linear_invs(e, phi)
        Q = q0_ * np.identity(3) + skew(q) + (q*q.transpose())/(1+q0_)
        print("determinant of rotation matrix",np.linalg.det(Q))
        print(Q)


    except:
        pass
