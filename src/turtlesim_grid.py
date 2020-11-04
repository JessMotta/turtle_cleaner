#!/usr/bin/env python

# version in python of cpp code turtlesim cleaner grid
# https://www.youtube.com/watch?v=ehH8oLfsz-w&feature=emb_title
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
        #callback function which is called when a message of type POse is recieved by the subscriber
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def degree2radians(self, angle_in_degrees):
        # convert degrees in radians
        return angle_in_degrees*pi/180

    def setDesiredOrientation(self, desired_angle_radians):
        # defines the desired orientation, and set true or false to clockwise
        relative_angle_radians = desired_angle_radians - self.pose.theta
        if(relative_angle_radians < 0):
            clockwise =  True
        else:
            clockwise = False
        
        self.rotate(abs(relative_angle_radians), abs(relative_angle_radians), clockwise)


    def getDistance(self, goal_pose):
        # euclidean distance between current pose and the goal
        return sqrt(pow((goal_pose.x - self.pose.x),2) + pow((goal_pose.y - self.pose.y), 2))

    def steering_angle(self, goal_pose):
        # return steering angle
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

    def angular_vel(self, goal_pose, constant=4):
        # return the angular velocity
        return constant*(self.steering_angle(goal_pose) - self.pose.theta)
     


    def move(self, speed, distance, isFoward):
        # to move straight
    
        if(isFoward):
           self.vel_msg.linear.x = abs(speed)
        else:
           self.vel_msg.linear.x = -abs(speed)
        
        self.vel_msg.linear.y = 0
        self.vel_msg.linear.z = 0

        self.vel_msg.angular.x = 0
        self.vel_msg.angular.y = 0
        self.vel_msg.angular.z = 0

        t0 = rospy.Time.now().to_sec()
        current_distance = 0

        # Loop to move the turtle  in an specified distance
        while(current_distance < distance):
            # Publish the velocity
            self.velocity_publisher.publish(self.vel_msg)
            # Take the actual time to velocity calculus
            t1 = rospy.Time.now().to_sec()
            # Calculates distancePoseStamped
            current_distance = speed*(t1-t0)

        # After the loop, stop the robot
        self.vel_msg.linear.x = 0
        # Force the robot to stop
        self.velocity_publisher.publish(self.vel_msg)


    def rotate(self, angular_speed, relative_angle, clockwise):
        # to rotate (left or right)
        self.vel_msg = Twist()

        self.vel_msg.linear.x = 0
        self.vel_msg.linear.y = 0
        self.vel_msg.linear.z = 0
        self.vel_msg.angular.x = 0
        self.vel_msg.angular.y = 0

        if(clockwise):
            # rotate to the right
            self.vel_msg.angular.z = -abs(angular_speed)
        else:
            # rotate to the left
           self.vel_msg.angular.z = abs(angular_speed)
        
        current_angle = 0
        t0 = rospy.Time.now().to_sec()

        while(current_angle < relative_angle):
            self.velocity_publisher.publish(self.vel_msg)
            t1 = rospy.Time.now().to_sec()
            current_angle = angular_speed*(t1-t0)

        self.vel_msg.angular.z = 0
        self.velocity_publisher.publish(self.vel_msg)
    
   


    def moveGoal(self, goal_pose, distance_tolerance):
        # send to a position that was defined

        while (self.getDistance(goal_pose) >= distance_tolerance):
            self.vel_msg.linear.x = 1.5*self.getDistance(goal_pose)
            self.vel_msg.linear.y = 0
            self.vel_msg.linear.z = 0

            self.vel_msg.angular.x = 0
            self.vel_msg.angular.y = 0
            self.vel_msg.angular.z = self.angular_vel(goal_pose)


            self.velocity_publisher.publish(self.vel_msg)

            # publish at the desired rate
            self.rate.sleep()
            
        
        self.vel_msg.linear.x = 0
        self.vel_msg.angular.z = 0
        self.velocity_publisher.publish(self.vel_msg)


    def gridClean(self):
        # make the grid with turtlesim
        goal_pose = Pose()

        goal_pose.x = 1
        goal_pose.y = 1
        goal_pose.theta = 0
        self.moveGoal(goal_pose, 0.01)
        self.setDesiredOrientation(0)

        self.move(2,9,True)
        rospy.sleep(1)
        self.rotate(self.degree2radians(10),self.degree2radians(90), False)
        rospy.sleep(1)
        self.move(2,9,True)
        rospy.sleep(1)
        self.rotate(self.degree2radians(10),self.degree2radians(90), False)
        rospy.sleep(1)
        self.move(2,1,True)
        rospy.sleep(1)
        self.rotate(self.degree2radians(30),self.degree2radians(90), False)
        rospy.sleep(1)
        self.move(2,9,True)
        rospy.sleep(1)
        self.rotate(self.degree2radians(30),self.degree2radians(90), True)
        rospy.sleep(1)
        self.move(2,1,True)
        rospy.sleep(1)
        self.rotate(self.degree2radians(30),self.degree2radians(90), True)
        rospy.sleep(1)
        self.move(2,9,True)
        print("Finished!!")


        rospy.spin()


if __name__ == "__main__":
    try:
        x = TurtleBot()
        x.gridClean()
    except rospy.ROSInterruptException:
         pass



             




    
