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

def user_input(s):
    user_in = raw_input(s)
    if 'y' in user_in.lower():
        return True
    else:
        return False

def main():
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('nimbus_test', anonymous=True)

    rospy.sleep(5.0)
    print "Subscribing... \n"

    test = nimbus_move()
    
    val = user_input("Ready? ")
    if val:
        test.grip_object(0.0)

    return 0

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

    # SCREWDRIVER
    target_pose1 = geometry_msgs.msg.Pose()
    target_pose1.position.x = -0.236 + 0.05
    target_pose1.position.y = 0.616
    target_pose1.position.z = 0.072

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

    target_pose1.orientation.x = -0.026
    target_pose1.orientation.y = -0.688
    target_pose1.orientation.z = 0.725
    target_pose1.orientation.w = -0.004

    # Move over pliers, lower arm and grip object in a partial grip
    test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
    target_pose1.position.x = target_pose1.position.x - 0.05
    test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
    test.grip_object(0.0)
    #test.grip_object(0.04)
    test.lower_raise_arm(0.266, execute_flag=True)

    #return 0

    # Move over to the second object to connect
    target_pose1.position.x = 0.309
    target_pose1.position.y = 0.437
    target_pose1.position.z = 0.328
    target_pose1.orientation.x = 0.488
    target_pose1.orientation.y = 0.529
    target_pose1.orientation.z = -0.488
    target_pose1.orientation.w = 0.495
    test.move_over_objects(target_pose1, plan_cartesian=False, execute_flag=True)
    test.grip_object(0.03)
    test.lower_raise_arm(target_pose1.position.z - 0.07, execute_flag=True)
    test.grip_object(0.0)
    test.lower_raise_arm(target_pose1.position.z + z_dist, execute_flag=True)

    # TESTINGG
    #test.grip_object(0.0)

    #return 0

    # Screwdriver test location
    test_pose = geometry_msgs.msg.Pose()
    test_pose.position.x = 0.532
    test_pose.position.y = 0.425
    test_pose.position.z = 0.266 + z_dist
    test_pose.orientation.x = 0.05
    test_pose.orientation.y = 0.685
    test_pose.orientation.z = 0.058
    test_pose.orientation.w = 0.725

    test.move_over_objects(test_pose, plan_cartesian=True, execute_flag=True)
    test.lower_raise_arm(0.264, execute_flag=True)

    rospy.sleep(5.0)

    # ROTATE JOINT
    jp = joint_poses()
    rospy.Subscriber('joint_states', JointState, jp.callback)

    rospy.sleep(5.0) # IMPORTANT!

    #print jp.joint_poses

    moveToJointPoseClient = actionlib.SimpleActionClient('nimbus_moveit/move_to_joint_pose', rail_manipulation_msgs.msg.MoveToJointPoseAction)
    moveToJointPoseClient.wait_for_server()

    jointPoseGoal = rail_manipulation_msgs.msg.MoveToJointPoseGoal()

    jointPoseGoal.joints = list(jp.joint_poses[0:6]) + [jp.joint_poses[6] + 1.5707]
    moveToJointPoseClient.send_goal(jointPoseGoal)
    moveToJointPoseClient.wait_for_result()
    result = moveToJointPoseClient.get_result()

    #moveToJointPoseClient = actionlib.SimpleActionClient('j2s7s300_driver/joints_action/joint_angles', kinova_msgs.msg.ArmJointAnglesAction)
    #moveToJointPoseClient.wait_for_server()

    #goal = kinova_msgs.msg.ArmJointAnglesGoal()
    #goal.angles.joint1 = jp.joint_poses[0]
    #goal.angles.joint2 = jp.joint_poses[1]
    #goal.angles.joint3 = jp.joint_poses[2]
    #goal.angles.joint4 = jp.joint_poses[3]
    #goal.angles.joint5 = jp.joint_poses[4]
    #goal.angles.joint6 = jp.joint_poses[5]
    #goal.angles.joint7 = jp.joint_poses[6] + 1.5707

    #moveToJointPoseClient.send_goal(goal)
    #moveToJointPoseClient.wait_for_result()

    return 0    

    '''user_in = user_input("Ready..?")
    if user_in:
        test.grip_object(0.04)

    rospy.sleep(7.0)

    target_pose1 = geometry_msgs.msg.Pose()
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

    # SCREWDRIVER FOR SQUEEGEE - LOWER SLIGHTLY
    target_pose1.position.x = -0.25
    target_pose1.position.y = 0.42
    target_pose1.position.z = 0.13

    test.move_over_objects(target_pose1, plan_cartesian=False, execute_flag=True)
    rospy.sleep(2.0)

    # PURPLE FOAM - LOWER
    target_pose1.position.x = 0.019 
    target_pose1.position.y = 0.411
    target_pose1.position.z = 0.16

    test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
    rospy.sleep(2.0)

    # RED FOAM - LOWER
    target_pose1.position.x = 0.254
    target_pose1.position.y = 0.412
    target_pose1.position.z = 0.18

    test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
    test.lower_raise_arm(0.29, execute_flag=True)
    rospy.sleep(2.0)

    # YELLOW FOAM - LOWER LOT MORE
    target_pose1.position.x = 0.315
    target_pose1.position.y = 0.638
    target_pose1.position.z = 0.157

    test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
    rospy.sleep(2.0)

    # WOOD LONG END POINT - RAISE LITTLE
    target_pose1.position.x = 0.016
    target_pose1.position.y = 0.638
    target_pose1.position.z = 0.14

    test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
    rospy.sleep(2.0)

    # GREEN FOAM - RAISE LITTLE
    target_pose1.position.x = -0.24
    target_pose1.position.y = 0.642
    target_pose1.position.z = 0.188

    test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
    rospy.sleep(2.0)

    return 0'''

    '''goal_pose = geometry_msgs.msg.Pose()
    test_pose = geometry_msgs.msg.Pose()
    target_pose1 = geometry_msgs.msg.Pose()
    target_pose2 = geometry_msgs.msg.Pose()

    # SPATULA
    #goal_pose.position.x = -0.2
    #goal_pose.position.y = 0.72
    #goal_pose.position.z = 0.06 
    #goal_pose.orientation.w = 1.0

    # SPOON
    goal_pose.position.x = 0.262
    goal_pose.position.y = 0.611
    goal_pose.position.z = 0.168 + 0.05
    goal_pose.orientation.x = 0.524
    goal_pose.orientation.y = 0.502
    goal_pose.orientation.z = -0.488
    goal_pose.orientation.w = -0.484

    #goal_pose.position.x = 0.361 #0.301
    #goal_pose.position.y = 0.624
    #goal_pose.position.z = 0.095 #0.09 #0.186
    #goal_pose.orientation.w = 1.0

    # SQUEEGEE
    #goal_pose.position.x = 0.315
    #goal_pose.position.y = 0.613
    #goal_pose.position.z = 0.213
    #goal_pose.orientation.x = -0.495
    #goal_pose.orientation.y = -0.476
    #goal_pose.orientation.z = 0.586
    #goal_pose.orientation.w = 0.43

    #target_pose1.position.x = -0.25
    #target_pose1.position.y = 0.51 - y_error
    #target_pose1.position.z = 0.06 + z_dist

    # SPATULA
    #target_pose1.position.x = 0.30
    #target_pose1.position.y = 0.51 - y_error 
    #target_pose1.position.z = 0.03 + z_dist

    # SPOON 
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
    test.lower_raise_arm(0.052, plan_cartesian=True, execute_flag=True)
    test.grip_object(0.03)
    #rospy.sleep(1.0)
    #test.grip_object(0.0)
    test.lower_raise_arm(0.25, plan_cartesian=True, execute_flag=True)

    #return 0
    target_pose2 = target_pose1
    target_pose2.position.x = -0.073
    target_pose2.position.y = 0.641
    target_pose2.position.z = 0.078

    test.move_over_objects(target_pose2, plan_cartesian=False, execute_flag=True)
    target_pose2.position.x = -0.053
    test.move_over_objects(target_pose2, plan_cartesian=False, execute_flag=True)
    test.grip_object(0.0)
    test.lower_raise_arm(0.25, plan_cartesian=True, execute_flag=True)
    test.grip_object(0.03)

    #return 0

    test.move_over_objects(goal_pose, plan_cartesian=False, execute_flag=True)
    test.lower_raise_arm(0.1, plan_cartesian=True, execute_flag=True)
    test.grip_object(0.0)

    #return 0

    # SPATULA
    #target_pose1.position.x = goal_pose.position.x
    #target_pose1.position.y = goal_pose.position.y
    #target_pose1.position.z = goal_pose.position.z
    #test.move_over_objects(target_pose1, execute_flag=True)

    #target_pose1.position.x = target_pose1.position.x - 0.035
    #test.move_over_objects(target_pose1, execute_flag=True)
    #test.grip_object(0.0)
    #test.lower_raise_arm(0.2, plan_cartesian=False, execute_flag=True)

    #test.move_over_objects(goal_pose, plan_cartesian=False, execute_flag=True)
    #test.lower_raise_arm(0.15, plan_cartesian=False, execute_flag=True)
    #test.lower_raise_arm(0.25, plan_cartesian=False, execute_flag=True)

    #return 0'''

    '''test_pose.position.x = 0.636
    test_pose.position.y = 0.412
    test_pose.position.z = 0.276
    test_pose.orientation.x = 0.635
    test_pose.orientation.y = 0.335
    test_pose.orientation.z = -0.443
    test_pose.orientation.w = 0.537'''

    # SPATULA
    #test_pose.position.x = 0.555
    #test_pose.position.y = 0.243
    #test_pose.position.z = 0.175
    #test_pose.orientation.x = 1
    #test_pose.orientation.y = 0.016
    #test_pose.orientation.z = 0.022
    #test_pose.orientation.w = 0.01

    #test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
    #rospy.sleep(10.0)
    #test_pose.position.y = 0.34
    #test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
    #test.lower_raise_arm(0.24, execute_flag=True)

    #test_pose.position.x = 0.602
    #test_pose.position.y = 0.375
    #test_pose.position.z = 0.173 + 0.1
    #test_pose.orientation.x = 0.544
    #test_pose.orientation.y = 0.463
    #test_pose.orientation.z = -0.494
    #test_pose.orientation.w = -0.495

    #test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
    #test.lower_raise_arm(0.173, plan_cartesian=False, execute_flag=True)
    #test_pose.position.z = 0.173
    #test_pose.position.y = 0.475
    #test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)

    '''test_pose = goal_pose
    test_pose.position.x = 0.612
    test_pose.position.y = 0.367
    test_pose.position.z = 0.299

    test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
    test.lower_raise_arm(0.109, plan_cartesian=True, execute_flag=True)
    test.lower_raise_arm(0.299, plan_cartesian=True, execute_flag=True)'''

    #return 0

    
    #result = moveToJointPoseClient.get_result()

    #if result.success:
    #    print "Successful \n"
    #else:
    #    print "Failed \n"


    #target_pose1.position.x -= 0.08
    #target_pose1.position.y = goal_pose.position.y - y_error
    #test.move_over_objects(target_pose1, execute_flag=True)
    #test.lower_raise_arm(0.15, execute_flag=True)
    #test.grip_object(0.0)
    #test.lower_raise_arm(0.25, execute_flag=True)

    
    
    
    #hammering_pose = geometry_msgs.msg.Pose()
    #hammering_pose.position.x = 0.505
    #hammering_pose.position.y = 0.341
    #hammering_pose.position.z = 0.390
    #hammering_pose.orientation.w = 1.0

    #test.move_over_objects(hammering_pose, execute_flag=True)

    #return 0

if __name__ == '__main__':
    main()
    moveit_commander.roscpp_shutdown()