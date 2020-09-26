#! /usr/bin/env python

import rospy
import sys
import moveit_commander

from nimbus_move import *

import moveit_msgs.msg
import rail_manipulation_msgs.msg
import geometry_msgs.msg
import actionlib
import copy

from tf.transformations import quaternion_from_euler
from sensor_msgs.msg import JointState

import kinova_msgs.msg


class joint_poses():
    def __init__(self):
        self.joint_poses = []

    def callback(self, data):
        self.joint_poses = data.position

def main():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('nimbus_test', anonymous=True)

    rospy.sleep(5.0)
    print "Subscribing... \n"

    test = nimbus_move()

    test.grip_object(0.0)
    #rospy.sleep(10.0)
    #test.grip_object(1.0)

    return 0

if __name__ == '__main__':
    main()
    moveit_commander.roscpp_shutdown()
