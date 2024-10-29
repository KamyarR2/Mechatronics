#!/usr/bin/python3

import rospy
from std_msgs.msg import Float64MultiArray
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen






    

def callback_func(msg):
    center = msg.data
    rospy.wait_for_service('turtle1/set_pen')
    pen_setter = rospy.ServiceProxy('turtle1/set_pen', SetPen)
    pen_setter(100, 0, 0, 0, 1)
    teleporter = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
    teleporter((center[0]*11), 11-(center[1]*11), 0.0)
    




if __name__ == '__main__':

    rospy.init_node('turtle_cam')

    
    turtle = rospy.Subscriber('/Hand_Pose',Float64MultiArray,callback=callback_func)
    rospy.spin()


    
            