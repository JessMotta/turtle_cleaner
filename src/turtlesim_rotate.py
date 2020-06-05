#!/usr/bin/env python

# code for rotate the turtlesim

import rospy
from geometry_msgs.msg import Twist
pi = 3.1415926535897

def rotate():
    # starts new node
    rospy.init_node('robot_cleaner',anonymous=True)
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    # receiving user's input
    print("Lets's rotate your turtle")
    speed = input("Input your turtle's speed: ")
    angle = input("Type your distance (degrees): ")
    clockwise = input("Clockwise?: ") # true or false

    #converting angles to radians
    angular_speed = speed*2*pi/360
    relative_angle = angle*2*pi/360

    # Don't use linear components
    vel_msg.linear.x = 0
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # check if your movement is clockwise or counterclockwise
    if(clockwise):
        vel_msg.angular.z = -abs(speed)
    else:
        vel_msg.angular.z = abs(speed)
    
    # setting current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0

    while(current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)
        
    # forcing the robot stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)
    rospy.spin()

if __name__ == "__main__":
    try:
        rotate()
    except rospy.ROSInterruptException:
        pass

    


