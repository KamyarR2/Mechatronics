#!/usr/bin/python3

import rospy
import cv2
import mediapipe as mp
from demo_pckg.srv import Service1,Service2

from std_msgs.msg import Float64MultiArray




def image_save(req) :
    global image
    cv2.imwrite("/home/kamiar/catkin_ws/src/demo_pckg/image.jpg",image)
    return True
def image_save_gray(req) :
    global image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("/home/kamiar/catkin_ws/src/demo_pckg/image_gray.jpg", gray_image) 
    return True



    
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles



if __name__ == '__main__':

    rospy.init_node('hand')
    service1 = rospy.Service('save_image_service',Service1, handler=image_save)
    service2 = rospy.Service('gray_image_service', Service2, handler=image_save_gray)


    pub = rospy.Publisher('Hand_Pose',Float64MultiArray,queue_size=10)

    with mp_hands.Hands(
                min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

        cap = cv2.VideoCapture(0)
        


        global image
        while cap.isOpened() :
                

                success, image = cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    break
                image = cv2.flip(image, 1)



                results = hands.process(image)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        landmarks = hand_landmarks.landmark

                        center_x = (landmarks[0].x + landmarks[5].x + landmarks[9].x + landmarks[13].x +landmarks[17].x+landmarks[1].x)/6

                        center_y = (landmarks[0].y + landmarks[5].y + landmarks[9].y + landmarks[13].y +landmarks[17].y+landmarks[1].y)/6
                    
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
                        cv2.circle(image, (int(center_x*image.shape[1]), int(center_y*image.shape[0])), 5, (200, 100, 200), -1)
                        center= Float64MultiArray()

                        center.data = [center_x , center_y]
                        pub.publish(center)
                        rate = rospy.Rate(1000)
                

                        rate.sleep()
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

      
    cap.release()
    cv2. destroyAllWindows()
            
                  
