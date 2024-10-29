from vpython import *
import numpy as np

import serial

scene.width = 1.8 * scene.width
scene.height = 2 * scene.height

box_roll = box(texture='image1.jpg', pos=vec(0, 1, 0),
               length=20, height=20, color=color.white)

arrow_roll = arrow(pos=vector(0, 1, 1), axis=vec(
    -1, 0, 0), shaftwidth=0.3, color=color.red)
arrow_roll.length = 8
L1 = label(pos=box_roll.pos,
                   text='Roll', xoffset=20,
                   yoffset=50, space=30,
                   height=16, border=4,
                   font='sans')


box_pitch = box(texture='image1.jpg', pos=vec(20, 1, 0),
                length=20, height=20, color=color.white)


arrow_pitch = arrow(pos=vector(19.8, 1, 1), axis=vec(
    -1, 0, 0), shaftwidth=0.3, color=color.red)
arrow_pitch.length = 8
L2 = label(pos=box_pitch.pos,
                   text='Pitch', xoffset=20,
                   yoffset=50, space=30,
                   height=16, border=4,
                   font='sans')

toRad = np.pi/180.0
toDeg = 1/toRad

# Simulate your object using VPython


arduinoData = serial.Serial('com9', 115200)


toRad = np.pi/180.0
toDeg = 1/toRad
while True:
    while arduinoData.inWaiting() == 0:
        pass
    dataPacket = arduinoData.readline()
    try:
        dataPacket = str(dataPacket, 'utf-8')
        splitPacket = dataPacket.split(",")
        roll = float(splitPacket[0])*toRad
        pitch = float(splitPacket[1])*toRad
        yaw = float(splitPacket[2])*toRad
        print(roll*toDeg, pitch*toDeg, yaw*toDeg)

        # Change the attributes of your object to syncronize it with real time motions
        arrow_roll.axis = vector(-cos(roll), sin(roll), 0)
        arrow_pitch.axis = vector(-cos(pitch), sin(pitch), 0)
        arrow_pitch.length = 8
        arrow_roll.length = 8
        

        


    except:
        pass
