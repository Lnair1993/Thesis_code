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
    '''print "Subscribing... \n"

    jp = joint_poses()
    rospy.Subscriber('joint_states', JointState, jp.callback)

    rospy.sleep(5.0) # IMPORTANT!

    print jp.joint_poses

    moveToJointPoseClient = actionlib.SimpleActionClient('nimbus_moveit/move_to_joint_pose', rail_manipulation_msgs.msg.MoveToJointPoseAction)
    moveToJointPoseClient.wait_for_server()

    jointPoseGoal = rail_manipulation_msgs.msg.MoveToJointPoseGoal()

    jointPoseGoal.joints = list(jp.joint_poses[0:6]) + [jp.joint_poses[6] + 1.5707]
    moveToJointPoseClient.send_goal(jointPoseGoal)
    moveToJointPoseClient.wait_for_result()
    result = moveToJointPoseClient.get_result()'''

    '''moveToJointPoseClient = actionlib.SimpleActionClient('j2s7s300_driver/joints_action/joint_angles', kinova_msgs.msg.ArmJointAnglesAction)
    moveToJointPoseClient.wait_for_server()

    goal = kinova_msgs.msg.ArmJointAnglesGoal()
    goal.angles.joint1 = jp.joint_poses[0]
    goal.angles.joint2 = jp.joint_poses[1]
    goal.angles.joint3 = jp.joint_poses[2]
    goal.angles.joint4 = jp.joint_poses[3]
    goal.angles.joint5 = jp.joint_poses[4]
    goal.angles.joint6 = jp.joint_poses[5]
    goal.angles.joint7 = jp.joint_poses[6] + 1.5707

    moveToJointPoseClient.send_goal(goal)
    moveToJointPoseClient.wait_for_result()
    result = moveToJointPoseClient.get_result()'''

    '''if result.success:
        print "Successful \n"
    else:
        print "Failed \n"'''


    # Gripper position definitions
    '''half_open = 0.04 #0.0 - 0.084 (close - open)
    full_close = 0.0
    full_open = 0.1

    target_pose1 = geometry_msgs.msg.Pose()

    target_pose1.position.x = 0.30 
    target_pose1.position.y = 0.51
    target_pose1.position.z = 0.03 + 0.25
    target_pose1.orientation.w = 1.0

    q = quaternion_from_euler(0, 3.14, 0)

    #obj_pose.position.x = 0.230132
    #obj_pose.position.y = -0.194576
    #obj_pose.position.z = 1.1979+0.25



    rospy.sleep(5.0)
    test = nimbus_move()
    target_pose1 = test.group.get_current_pose().pose
    target_pose1.orientation.x = q[0]
    target_pose1.orientation.y = q[1]
    target_pose1.orientation.z = q[2]
    target_pose1.orientation.w = q[3]

    rospy.sleep(5.0) # IMPORTANT
    test.move_over_objects(target_pose1, plan_cartesian=True)
    #test.lower_raise_arm(0.1, execute_flag=True)

    print "Initialization complete \n"
    test.grip_object(full_close)
    rospy.sleep(2.0)
    test.grip_object(half_open)
    rospy.sleep(2.0)
    test.grip_object(full_open)'''

    y_error = 0.09
    z_dist = 0.15
    gripper_orientation = True
    test = nimbus_move()

    goal_pose = geometry_msgs.msg.Pose()
    target_pose1 = geometry_msgs.msg.Pose()

    goal_pose.position.x = -0.2
    goal_pose.position.y = 0.72
    goal_pose.position.z = 0.06 
    goal_pose.orientation.w = 1.0

    target_pose1.position.x = 0.30; 
    target_pose1.position.y = 0.51 - y_error 
    target_pose1.position.z = 0.03 + z_dist

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
    test.lower_raise_arm(0.031, execute_flag=True)
    test.grip_object(0.06)
    test.lower_raise_arm(0.25, execute_flag=True)
    
    target_pose1.position.x -= 0.08
    target_pose1.position.y = goal_pose.position.y - y_error
    test.move_over_objects(target_pose1, execute_flag=True)
    test.lower_raise_arm(0.15, execute_flag=True)
    test.grip_object(0.0)
    test.lower_raise_arm(0.25, execute_flag=True)

    hammering_pose = geometry_msgs.msg.Pose()
    hammering_pose.position.x = 0.505
    hammering_pose.position.y = 0.341
    hammering_pose.position.z = 0.390
    hammering_pose.orientation.w = 1.0

    test.move_over_objects(hammering_pose, execute_flag=True)

    return 0

if __name__ == '__main__':
    main()
    moveit_commander.roscpp_shutdown()