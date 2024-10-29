import time
import serial
import numpy as np
import matplotlib.pyplot as plt
import math


arduinoData = serial.Serial('com9', 115200)
time.sleep(1)

toRad = np.pi / 180.0
toDeg = 1 / toRad


def skew(x):
    return np.array([[0, -x[2][0], x[1][0]],
                     [x[2][0], 0, -x[0][0]],
                     [-x[1][0], x[0][0], 0]])
def vect(Q):
    return 0.5*np.array([[Q[2][1]-Q[1][2]],
                    [Q[0][2]-Q[2][0]],
                    [Q[1][0]-Q[0][1]]])

def trace(Q):
    return (Q[0][0] + Q[1][1] + Q[2][2]);


def natural_parameters(roll , pitch , yaw):
    x = np.array([[1], [0], [0]])
    y = np.array([[0], [1], [0]])
    z = np.array([[0], [0], [1]])

    Qx = x * x.transpose() + math.cos(roll)*(np.identity(3) - x *
                                             x.transpose()) + math.sin(roll)*skew(x)
    Qy = y * y.transpose() + math.cos(pitch)*(np.identity(3) - y *
                                             y.transpose()) + math.sin(pitch)*skew(y)
    Qz = z * z.transpose() + math.cos(yaw)*(np.identity(3) - z *
                                             z.transpose()) + math.sin(yaw)*skew(z)
    return Qx , Qy , Qz;




while True:
    while arduinoData.inWaiting() == 0:
        pass
    dataPacket = arduinoData.readline()
    try:
        dataPacket = str(dataPacket, 'utf-8')
        splitPacket = dataPacket.split(",")
        roll = float(splitPacket[0]) * toRad
        pitch = float(splitPacket[1]) * toRad
        yaw = float(splitPacket[2]) * toRad
        print(roll, pitch, yaw)
        Qx , Qy , Qz = natural_parameters(roll , pitch , yaw)

        Q = np.dot(Qz,Qy,Qx)


        phi = math.acos((trace(Q)-1)/2)

        e = vect(Q)/math.sin(phi)
        print(phi)
        print(e)
        

      
    except:
        pass



