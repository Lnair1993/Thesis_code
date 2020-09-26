# All the tests for the different tools
# Take locations of all objects
# Take ordering/rankings of objects
# Need to check transform from attachment locations

import rospy
import sys
import moveit_commander
import geometry_msgs.msg
import actionlib
import rail_manipulation_msgs.msg

from nimbus_move import *

class nimbus_tools():
    def __init__(self, obj_poses, obj_ranking, tool_name, default_poses=True):
        self.object_poses = obj_poses
        self.object_ranking = obj_ranking
        self.default_poses = default_poses
        
        self.tool_demo(tool_name)
        moveit_commander.roscpp_shutdown()

        # Call the test corresponding to the tool name

    def gripper_orient(self, gripper_orientation, target_pose1):
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
    
        return target_pose1

    def user_input(self, s):
        user_in = raw_input(s)
        if 'y' in user_in.lower():
            return True
        else:
            return False

    def tool_demo(self, tool_name):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('nimbus_cases', anonymous=True)
        print "Initializing environment... \n"
        rospy.sleep(5.0)

        test = nimbus_move()

        y_error = 0.09
        z_dist = 0.15

        if 'spoon' in tool_name.lower():
            if self.default_poses: # Use pre-defined poses
                # First target location
                target_pose1 = geometry_msgs.msg.Pose()
                target_pose1.position.x = -0.172
                target_pose1.position.y = 0.614
                target_pose1.position.z = 0.121
                target_pose1 = self.gripper_orient(True, target_pose1)

                test.move_over_objects(target_pose1, plan_cartesian=False, execute_flag=True)
                test.lower_raise_arm(0.052, plan_cartesian=True, execute_flag=True)
                test.grip_object(0.03)
                test.lower_raise_arm(0.25, plan_cartesian=True, execute_flag=True)

                # Second target location
                target_pose2 = geometry_msgs.msg.Pose()
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

                # Third target location
                goal_pose = geometry_msgs.msg.Pose()
                goal_pose.position.x = 0.262
                goal_pose.position.y = 0.611
                goal_pose.position.z = 0.218
                goal_pose.orientation.x = 0.524
                goal_pose.orientation.y = 0.502
                goal_pose.orientation.z = -0.488
                goal_pose.orientation.w = -0.484

                test.move_over_objects(goal_pose, plan_cartesian=False, execute_flag=True)
                test.lower_raise_arm(0.1, plan_cartesian=True, execute_flag=True)
                test.grip_object(0.0)

                # Testing location
                test_pose = geometry_msgs.msg.Pose()
                test_pose = goal_pose
                test_pose.position.x = 0.612
                test_pose.position.y = 0.367
                test_pose.position.z = 0.299

                test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
                test.lower_raise_arm(0.109, plan_cartesian=True, execute_flag=True)
                test.lower_raise_arm(0.299, plan_cartesian=True, execute_flag=True)

                return 0

        elif 'spatula' in tool_name.lower():
            if self.default_poses:
                # First target location
                target_pose1 = geometry_msgs.msg.Pose()
                target_pose1.position.x = 0.30
                target_pose1.position.y = 0.51 - y_error 
                target_pose1.position.z = 0.03 + z_dist
                target_pose1 = self.gripper_orient(True, target_pose1)

                test.move_over_objects(target_pose1, plan_cartesian=False, execute_flag=True)
                test.lower_raise_arm(0.048, execute_flag=True)
                test.grip_object(0.027)
                test.lower_raise_arm(0.25, plan_cartesian=False, execute_flag=True)

                # Second target location
                goal_pose = geometry_msgs.msg.Pose()
                goal_pose.position.x = 0.361 #0.301
                goal_pose.position.y = 0.624
                goal_pose.position.z = 0.095 #0.09 #0.186
                goal_pose.orientation.w = 1.0

                target_pose1.position.x = goal_pose.position.x
                target_pose1.position.y = goal_pose.position.y
                target_pose1.position.z = goal_pose.position.z
                test.move_over_objects(target_pose1, execute_flag=True)

                target_pose1.position.x = target_pose1.position.x - 0.035
                test.move_over_objects(target_pose1, execute_flag=True)
                test.grip_object(0.0)
                test.lower_raise_arm(0.2, plan_cartesian=False, execute_flag=True)

                # Testing location
                test_pose.position.x = 0.555
                test_pose.position.y = 0.243
                test_pose.position.z = 0.175
                test_pose.orientation.x = 1
                test_pose.orientation.y = 0.016
                test_pose.orientation.z = 0.022
                test_pose.orientation.w = 0.01

                test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
                rospy.sleep(10.0)
                test_pose.position.y = 0.34
                test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
                test.lower_raise_arm(0.24, execute_flag=True)

                return 0

        elif 'squeegee' in tool_name.lower():
            # First target location
            target_pose1 = geometry_msgs.msg.Pose()
            target_pose1.position.x = -0.25
            target_pose1.position.y = 0.51 - y_error
            target_pose1.position.z = 0.06 + z_dist
            target_pose1 = self.gripper_orient(True, target_pose1)

            test.move_over_objects(target_pose1, plan_cartesian=False, execute_flag=True)
            test.lower_raise_arm(0.052, execute_flag=True)
            test.grip_object(0.0)
            test.lower_raise_arm(0.25, plan_cartesian=False, execute_flag=True)

            # Second target location
            goal_pose = geometry_msgs.msg.Pose()
            goal_pose.position.x = 0.315
            goal_pose.position.y = 0.613
            goal_pose.position.z = 0.213
            goal_pose.orientation.x = -0.495
            goal_pose.orientation.y = -0.476
            goal_pose.orientation.z = 0.586
            goal_pose.orientation.w = 0.43

            test.move_over_objects(goal_pose, plan_cartesian=False, execute_flag=True)
            test.lower_raise_arm(0.15, plan_cartesian=False, execute_flag=True)
            test.lower_raise_arm(0.25, plan_cartesian=False, execute_flag=True)

            # Testing location
            test_pose = geometry_msgs.msg.Pose()
            test_pose.position.x = 0.602
            test_pose.position.y = 0.375
            test_pose.position.z = 0.173 + 0.1
            test_pose.orientation.x = 0.544
            test_pose.orientation.y = 0.463
            test_pose.orientation.z = -0.494
            test_pose.orientation.w = -0.495

            test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)
            test.lower_raise_arm(0.173, plan_cartesian=False, execute_flag=True)
            test_pose.position.z = 0.173
            test_pose.position.y = 0.475
            test.move_over_objects(test_pose, plan_cartesian=False, execute_flag=True)

            return 0

        elif 'screwdriver' in tool_name.lower():
            target_pose1 = geometry_msgs.msg.Pose()
            target_pose1.position.x = -0.236 + 0.05
            target_pose1.position.y = 0.616
            target_pose1.position.z = 0.072
            target_pose1.orientation.x = -0.026
            target_pose1.orientation.y = -0.688
            target_pose1.orientation.z = 0.725
            target_pose1.orientation.w = -0.004

            # Move over pliers, lower arm and grip object in a partial grip
            test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
            target_pose1.position.x = target_pose1.position.x - 0.05
            test.move_over_objects(target_pose1, plan_cartesian=True, execute_flag=True)
            test.grip_object(0.0)
            test.lower_raise_arm(0.266, execute_flag=True)

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

            moveToJointPoseClient = actionlib.SimpleActionClient('nimbus_moveit/move_to_joint_pose', rail_manipulation_msgs.msg.MoveToJointPoseAction)
            moveToJointPoseClient.wait_for_server()

            jointPoseGoal = rail_manipulation_msgs.msg.MoveToJointPoseGoal()

            jointPoseGoal.joints = list(jp.joint_poses[0:6]) + [jp.joint_poses[6] + 1.5707]
            moveToJointPoseClient.send_goal(jointPoseGoal)
            moveToJointPoseClient.wait_for_result()
            result = moveToJointPoseClient.get_result()

            return 0

        
        else:
            # Normal sensing code
            user_in = self.user_input("Ready..?")
            if user_in:
                test.grip_object(0.04)

            rospy.sleep(7.0)

            target_pose1 = geometry_msgs.msg.Pose()
            target_pose1 = self.gripper_orient(True, target_pose1)

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

            return 0


        
