#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn
import math
import numpy as np
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import TeleportRelative
from turtlesim.srv import SetPen
from turtlesim.msg import Pose
from turtle import Screen



def move_turtle_linear(turtle_name, linear_speed, distance,direction):
    

    pub = rospy.Publisher(turtle_name + '/cmd_vel', Twist, queue_size=10)
    

    index = np.nonzero(linear_speed)[0][0]


    vel_msg = Twist()
    if index==0 :
        vel_msg.linear.x = direction*linear_speed[index]
        speed = abs(vel_msg.linear.x) 
        
    elif index==1 :
        vel_msg.linear.y = direction*linear_speed[index]
        speed = abs(vel_msg.linear.y)
    else:
        vel_msg.linear.z = direction*linear_speed[index]
        speed = abs(vel_msg.linear.z)




    duration = distance / speed 

    rate = rospy.Rate(10) # 10 Hz
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < duration:
        pub.publish(vel_msg)
        rate.sleep()

    vel_msg.linear.x = 0
    pub.publish(vel_msg)

def move_turtle_angular(turtle_name, angular_speed, angle,direction) :
    pub = rospy.Publisher(turtle_name + '/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    vel_msg.angular.z = direction*angular_speed
    angle = math.radians(angle)
    duration = angle / abs(vel_msg.angular.z)

    rate = rospy.Rate(10)
    start_time = rospy.Time.now().to_sec()
    while rospy.Time.now().to_sec() - start_time < duration:
        pub.publish(vel_msg)
        rate.sleep()

    vel_msg.linear.x = 0
    pub.publish(vel_msg)
    
    



if __name__ == '__main__':

    rospy.init_node('turtlesim_move3')


    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)

    spawner(0.3, 4.4, 0.0, 'turtle3')
    rospy.wait_for_service('turtle3/set_pen')
    pen_setter = rospy.ServiceProxy('turtle3/set_pen', SetPen)
    pen_setter(255, 0, 0, 4, 0)

    teleporter = rospy.ServiceProxy('turtle3/teleport_relative', TeleportRelative)
    teleporter(0.0, 90.0 * math.pi / 180)
    move_turtle_linear('turtle3',[1,0,0],2.6,1)
    teleporter(0.0, -180.0 * math.pi / 180)
    move_turtle_linear('turtle3',[1,0,0],1.2,1)
    teleporter(0.0, 50.0 * math.pi / 180)
    move_turtle_linear('turtle3',[1,0,0],1.6,1)
    teleporter(0.0, 180.0 * math.pi / 180)
    move_turtle_linear('turtle3',[1,0,0],1.6,1)
    teleporter(0.0, -90.0 * math.pi / 180)
    move_turtle_linear('turtle3',[1,0,0],1.6,1)
    move_turtle_linear('turtle3',[1,0,0],1.6,-1)
    teleporter(0.0, 40.0 * math.pi / 180)
    pen_setter(0, 0, 0, 4, 1)
    move_turtle_linear('turtle3',[1,0,0],1.7,-1)






    

