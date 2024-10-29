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

    rospy.init_node('turtlesim_move7')


    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', Spawn)

    spawner(3, 4.4, 0.0, 'turtle7')
    rospy.wait_for_service('turtle7/set_pen')
    pen_setter = rospy.ServiceProxy('turtle7/set_pen', SetPen)
    pen_setter(0, 255, 0, 4, 0)

    move_turtle_linear('turtle7',[1,0,0],0.5,1)
    move_turtle_linear('turtle7',[1,0,0],1,-1)
    move_turtle_linear('turtle7',[1,0,0],0.455,1)
    move_turtle_linear('turtle7',[0,1,0],2.1,1)
    move_turtle_linear('turtle7',[1,0,0],0.5,1)
    move_turtle_linear('turtle7',[1,0,0],1,-1)
    move_turtle_linear('turtle7',[1,0,0],0.5,1)
    move_turtle_angular('turtle7',1,85,1)

    pen_setter(0, 0, 0, 4, 1)
    move_turtle_linear('turtle7',[1,0,0],0.8,1)

 






    

