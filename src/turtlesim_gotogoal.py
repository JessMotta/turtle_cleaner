#!/usr/bin/env python

# code to send the turtlesim to a position

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class TurtleBot():

    def __init__(self):
        # starts a node
        rospy.init_node('turtlebot_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        # subscriber
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        #callback function which is called when a message of type POse is received by the subscriber
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def euclidean_distance(self, goal_pose):
        # euclidean distance between current pose and the goal
        return sqrt(pow((goal_pose.x -self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
    
    def linear_vel(self, goal_pose, constant=1.5):
        #return linear velocity mult by constant
        return constant*self.euclidean_distance(goal_pose)

    def steering_angle(self, goal_pose):
        # return steering angle
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
    
    def angular_vel(self, goal_pose, constant=6):
        return constant*(self.steering_angle(goal_pose) - self.pose.theta)
    
    def move2goal(self):
        # moves the turtle to goal
        goal_pose = Pose()

        # get the user's input
        goal_pose.x = input("set you X goal: ")
        goal_pose.y = input("set you Y goal: ")

        distance_tolerance = input("set your distance tolerance: ")

        vel_msg = Twist()

        while self.euclidean_distance(goal_pose) >= distance_tolerance:
            # linear velocity in x axis
            vel_msg.linear.x = self.linear_vel(goal_pose)
            vel_msg.linear.y = 0 
            vel_msg.linear.z = 0

            # angular velocity z-axis
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0 
            vel_msg.angular.z = self.angular_vel(goal_pose)  

            # publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # publish at the desired rate
            self.rate.sleep()

        # stop the robot's movement
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
        print(" Goal reached")

        # if press ctrl + c, the node will stop
        rospy.spin()

if __name__ == "__main__":
    try:
        x = TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
         pass



             




    
