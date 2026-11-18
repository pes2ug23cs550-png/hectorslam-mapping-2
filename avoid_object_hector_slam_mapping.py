#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

move = Twist()

def callback(msg):
    global move

    # Take front distance
    front = min(min(msg.ranges[0:10]), min(msg.ranges[-10:]))

    if front < 0.6:
        # Obstacle detected → turn
        move.linear.x = 0.0
        move.angular.z = 0.5
    else:
        # Free → move forward
        move.linear.x = 0.2
        move.angular.z = 0.0

def main():
    rospy.init_node('auto_move')
    rospy.Subscriber('/scan', LaserScan, callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        pub.publish(move)
        rate.sleep()

if __name__ == '__main__':
    main()