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

    y_error = 0.09
    z_dist = 0.15
    z_dist_short = 0.04
    gripper_orientation = True
    test = nimbus_move()

    goal_pose = geometry_msgs.msg.Pose()
    test_pose = geometry_msgs.msg.Pose()
    target_pose1 = geometry_msgs.msg.Pose()
    target_pose2 = geometry_msgs.msg.Pose()

    # SQUEEGEE ----------------------------------------------------------------------------------------------------------
    goal_pose.position.x = 0.28
    goal_pose.position.y = 0.504 - y_error
    goal_pose.position.z = 0.213
    goal_pose.orientation.x = -0.495
    goal_pose.orientation.y = -0.476
    goal_pose.orientation.z = 0.586
    goal_pose.orientation.w = 0.43

    target_pose1.position.x = -0.25
    target_pose1.position.y = 0.51 - y_error
    target_pose1.position.z = 0.06 + z_dist

    if gripper_orientation:
        target_pose1.orientation.x = 0.489
        target_pose1.orientation.y = 0.522
        target_pose1.orientation.z = -0.489
        target_pose1.orientation.w = 0.5
    else:
        target_pose1.orientation.x = -0.006 
        target_pose1.orientation.y = 0.704
        target_pose1.orientation.z = -0.015
        target_pose1.orientation.w = 0.71


    test.move_over_objects(target_pose1, plan_cartesian=False, execute_flag=True)
    test.lower_raise_arm(0.052, execute_flag=True)
    test.grip_object(0.0)
    test.lower_raise_arm(0.28, plan_cartesian=True, execute_flag=True) # WAS FALSE

    test.move_over_objects(goal_pose, plan_cartesian=False, execute_flag=True)
    test.lower_raise_arm(0.15, plan_cartesian=True, execute_flag=True) # WAS FALSE
    test.lower_raise_arm(0.25, plan_cartesian=True, execute_flag=True) # WAS FALSE

    test_pose.position.x = 0.602
    test_pose.position.y = 0.375
    test_pose.position.z = 0.173 + 0.1
    test_pose.orientation.x = 0.544
    test_pose.orientation.y = 0.463
    test_pose.orientation.z = -0.494
    test_pose.orientation.w = -0.495

    test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
    test.lower_raise_arm(0.173, plan_cartesian=True, execute_flag=True) # WAS FALSE
    test_pose.position.z = 0.173
    test_pose.position.y = 0.475
    test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)

    test.grip_object(1.0)
    test.lower_raise_arm(0.25, plan_cartesian=True, execute_flag=True) # WAS FALSE

    # SPATULA ------------------------------------------------------------------------------------------------------------
    goal_pose.position.x = 0.262
    goal_pose.position.y = 0.611
    goal_pose.position.z = 0.168 + 0.05
    goal_pose.orientation.x = 0.489
    goal_pose.orientation.y = 0.522
    goal_pose.orientation.z = -0.489
    goal_pose.orientation.w = 0.5

    target_pose1.position.x = -0.172
    target_pose1.position.y = 0.614
    target_pose1.position.z = 0.121

    if gripper_orientation:
        target_pose1.orientation.x = 0.489
        target_pose1.orientation.y = 0.522
        target_pose1.orientation.z = -0.489
        target_pose1.orientation.w = 0.5
    else:
        target_pose1.orientation.x = -0.006 
        target_pose1.orientation.y = 0.704
        target_pose1.orientation.z = -0.015
        target_pose1.orientation.w = 0.71

    test.move_over_objects(target_pose1, plan_cartesian=False, execute_flag=True)
    test.lower_raise_arm(0.052 + z_dist_short, plan_cartesian=True, execute_flag=True)
    test.grip_object(0.0)
    #rospy.sleep(1.0)
    #test.grip_object(0.0)
    test.lower_raise_arm(0.25, plan_cartesian=True, execute_flag=True)

    test.move_over_objects(goal_pose, plan_cartesian=False, execute_flag=True)
    test.lower_raise_arm(0.103, plan_cartesian=True, execute_flag=True)
    #test.grip_object(0.0)
    
    test_pose.position.x = -0.605
    test_pose.position.y = 0.398
    test_pose.position.z = 0.299
    test_pose.orientation.x = 0.489
    test_pose.orientation.y = 0.522
    test_pose.orientation.z = -0.489
    test_pose.orientation.w = 0.5

    test.move_over_objects(test_pose, plan_cartesian=True, execute_flag=True)
    test.lower_raise_arm(0.109 + z_dist_short, plan_cartesian=True, execute_flag=True)
    test.grip_object(1.0)
    test.lower_raise_arm(0.299, plan_cartesian=True, execute_flag=True)

    return 0

if __name__ == '__main__':
    main()
    moveit_commander.roscpp_shutdown()
