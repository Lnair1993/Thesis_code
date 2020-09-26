# Define classes and function for moving Nimbus

import rospy
import moveit_commander
import moveit_msgs.msg
import rail_manipulation_msgs.msg
import geometry_msgs.msg
import actionlib
import copy

from tf import TransformListener

class nimbus_move():
    def __init__(self, view_plan = True):
        self.robot = moveit_commander.RobotCommander()
        self.group = moveit_commander.MoveGroupCommander("arm")    
        self.gripperGoal = rail_manipulation_msgs.msg.GripperGoal()
        self.listener = TransformListener() # For transforming object poses
        
        self.gripper_client = actionlib.SimpleActionClient('gripper_actions/gripper_manipulation', rail_manipulation_msgs.msg.GripperAction)
        self.gripper_client.wait_for_server()
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
        
        self.display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        self.view_plan = view_plan 

    def plan_view(self, plan1):
        self.display_trajectory.trajectory_start = self.robot.get_current_state()
        self.display_trajectory.trajectory.append(plan1)
        self.display_trajectory_publisher.publish(self.display_trajectory)
        rospy.sleep(5)

    def move_over_objects(self, object_location, plan_cartesian = True, execute_flag = False, eef_step = 0.01, jump_threshold = 0.0):
        # Call the sense-predict function here and add wait
        # Returns list corresponding to material pierceability

        # Transform object pose to table base link frame
        #object_location = self.obj_pose_tf(object_location)

        if not plan_cartesian:
            self.group.set_pose_target(object_location)
            plan1 = self.group.plan()
        else:
            waypoints = []
            waypoints.append(self.group.get_current_pose().pose)
            waypoints.append(copy.deepcopy(object_location))
            (plan1, fraction) = self.group.compute_cartesian_path(waypoints, eef_step, jump_threshold, avoid_collisions=False)

            # Check if cartesian path successfully computed
            if fraction == 0.0:
                print "Could not compute Cartesian path \n"
            else:
                print "Successfully computed Cartesian path \n"
        
        if self.view_plan:
            self.plan_view(plan1)

        if execute_flag:
            self.group.execute(plan1, wait = True)

    def lower_raise_arm(self, lower_dist, plan_cartesian = True, execute_flag = False, eef_step = 0.01, jump_threshold = 0.0):
        # Lower arm to lower pose - also used for pierce attach and raising arm
        current_pose = self.group.get_current_pose().pose
        new_pose = geometry_msgs.msg.Pose()

        # Set the new position
        new_pose.position.x = current_pose.position.x
        new_pose.position.y = current_pose.position.y
        new_pose.position.z = lower_dist
        new_pose.orientation.x = current_pose.orientation.x
        new_pose.orientation.y = current_pose.orientation.y
        new_pose.orientation.z = current_pose.orientation.z
        new_pose.orientation.w = current_pose.orientation.w

        if not plan_cartesian:
            self.group.set_pose_target(new_pose)
            plan1 = self.group.plan()
        else:
            waypoints = []
            waypoints.append(current_pose)
            waypoints.append(new_pose)
            (plan1, fraction) = self.group.compute_cartesian_path(waypoints, eef_step, jump_threshold, avoid_collisions=False)

            # Check if cartesian path successfully computed
            if fraction == 0.0:
                print "Could not compute Cartesian path \n"
            else:
                print "Successfully computed Cartesian path \n"

        if self.view_plan:
            self.plan_view(plan1)
        
        if execute_flag:
            self.group.execute(plan1, wait = True)

    def grip_object(self, gripper_close):
        # For pliers and tongs, only partially close gripper - pass gripper_close = 50.0
        # Also used for grasp attach
        self.gripperGoal.position = gripper_close
        self.gripperGoal.force = 155

        self.gripper_client.send_goal(self.gripperGoal)
        self.gripper_client.wait_for_result()
        result = self.gripper_client.get_result()

        if result:
            print "Grip successful \n"
        else:
            print "Grip failed \n"

    def obj_pose_tf(self, object_pose):
    # Transform pose from camera_optical_frame to table_base_link
        #listener = TransformListener()

        pose_init = geometry_msgs.msg.PoseStamped()
        pose_init.header.frame_id = 'camera_rgb_optical_frame'
        pose_init.header.stamp = rospy.Time()
        pose_init.pose.position.x = object_pose.position.x
        pose_init.pose.position.y = object_pose.position.y
        pose_init.pose.position.z = object_pose.position.z

        pose_init = self.listener.transformPose('table_base_link', pose_init)

        pose_tf = geometry_msgs.msg.Pose()
        pose_tf.position.x = pose_init.pose.position.x
        pose_tf.position.y = pose_init.pose.position.y
        pose_tf.position.z = pose_init.pose.position.z

        return pose_tf






