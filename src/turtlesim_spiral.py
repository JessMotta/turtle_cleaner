#!/usr/bin/env python

# version in python of cpp code turtlesim cleaner spiral
# https://www.youtube.com/watch?v=ehH8oLfsz-w
# author: Jessica Lima Motta 
# github: https://github.com/JessMotta

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
pi =  3.1415926535897


class TurtleBot():

    def __init__(self):
        # starts a node
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        # subscriber
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.poseCallback)

        self.pose = Pose()
        self.rate = rospy.Rate(10)
        self.vel_msg = Twist()

        print('****** START TESTING ******' )
    

    def poseCallback(self, data):
        #callback function which is called when a message of type POse is received by the subscriber
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)


    def spiralClean(self):
        # print a spiral with turtlesim
        constant_speed = 4
        vk = 1
        wk = 2
        rk = 0.5

        rospy.sleep(1)

        while((self.pose.x < 10.5) and (self.pose.y < 10.5)):
            rk = rk + 0.1 # it's different to 
            self.vel_msg.linear.x = rk
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0

            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.angular.z = constant_speed


            self.velocity_publisher.publish(self.vel_msg)
            print('vel_msg.linear.x = ' + str(self.vel_msg.linear.x))
            print('vel_msg.angular.z = ' + str(self.vel_msg.angular.z))

            #vk = self.vel_msg.linear.x
		    #wk = self.vel_msg.angular.z
		    #rk = vk/wk

            # publish at the desired rate
            self.rate.sleep()
            print('rk = ' + str(rk))
            print('vk = ' + str(vk))
            print('wk = ' + str(wk))

            
        
        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0
        self.velocity_publisher.publish(self.vel_msg)

        print("Finished!!")

    # If we press control + C, the node will stop.
        rospy.spin()


if __name__ == "__main__":
    try:
        x = TurtleBot()
        x.spiralClean()
    except rospy.ROSInterruptException:
         pass



             




    
