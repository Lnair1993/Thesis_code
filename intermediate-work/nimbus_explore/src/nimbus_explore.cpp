#include <ros/ros.h>

#include <iostream>
#include <string.h>
#include <stdio.h>
#include <fstream>

#include <moveit/move_group_interface/move_group.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>

#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>

#include <rail_manipulation_msgs/GripperAction.h>
#include <actionlib/client/simple_action_client.h>
#include <rail_manipulation_msgs/LiftAction.h>

#include <geometry_msgs/PointStamped.h>
#include <tf/transform_listener.h>

// Use system pipeline for writing the code
// Write it in rospy so reading/writing from/to files is easier
// Define a function for sensing of object properties
// Define a function for performing grasping
// Define a function for performing piercing

int main(int argc, char **argv)
{
  ros::init(argc, argv, "nimbus_explore");
  ros::NodeHandle node_handle;  
  ros::AsyncSpinner spinner(1);
  spinner.start();
  ROS_INFO("Initializing Move to Pose...");

  ros::Publisher display_publisher = node_handle.advertise<moveit_msgs::DisplayTrajectory>("/move_group/display_planned_path", 1, true);
  moveit_msgs::DisplayTrajectory display_trajectory;

  actionlib::SimpleActionClient<rail_manipulation_msgs::GripperAction> gripperClient("gripper_actions/gripper_manipulation");
  rail_manipulation_msgs::GripperGoal gripperGoal;
  
  // Transformation listener
  tf::TransformListener listener(ros::Duration(10));

  /* This sleep is ONLY to allow Rviz to come up */
  sleep(5.0);
  
  // The group being controlled
  moveit::planning_interface::MoveGroup group("arm"); //gripper or arm
  moveit::planning_interface::PlanningSceneInterface planning_scene_interface;  

  // We can print the name of the reference frame and end-effector for this robot.
  ROS_INFO("Reference frame: %s", group.getPlanningFrame().c_str());
  ROS_INFO("End-effector link: %s", group.getEndEffectorLink().c_str());

  const float gripper_open = 100.0;
  const float gripper_close = 0.0;

  geometry_msgs::Pose target_pose1;

  target_pose1.position.x = 0.30; 
  target_pose1.position.y = 0.51; 
  target_pose1.position.z = 0.03;
  target_pose1.orientation.w = 1.0;

  group.setPoseTarget(target_pose1);
  group.setGoalOrientationTolerance(0.1);


  moveit::planning_interface::MoveGroup::Plan my_plan;

  sleep(10.0); //Give some time to initialize everything before starting the planner

  bool success = group.plan(my_plan);

  ROS_INFO("Visualizing plan 1: Move above object (pose goal) %s",success?"":"FAILED");    
  // Sleep to give Rviz time to visualize the plan. 
  sleep(5.0);

  // Visualizing plans
  // ^^^^^^^^^^^^^^^^^
  // Now that we have a plan we can visualize it in Rviz.  This is not
  // necessary because the group.plan() call we made above did this
  // automatically.  But explicitly publishing plans is useful in cases that we
  // want to visualize a previously created plan.
  if (0)
  {
    ROS_INFO("Visualizing plan 1 (again)");    
    display_trajectory.trajectory_start = my_plan.start_state_;
    display_trajectory.trajectory.push_back(my_plan.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }


  ROS_INFO("Attempting to close gripper.. \n");

  gripperGoal.position = 0.04;
  gripperGoal.force = 100;

  gripperClient.sendGoal(gripperGoal);
  gripperClient.waitForResult(ros::Duration(10.0));
  if (!gripperClient.getResult()->success)
  {
    ROS_INFO("Closing gripper failed.");
    return 0;
  }

  ROS_INFO("Successfully closed gripper. \n");


  return 0;


  std::string output_filepath = "/home/lnair3/pierce_data/data.csv";

  // Initialize object positions
  geometry_msgs::Pose tool_pose;
  std::vector<geometry_msgs::Pose> object_poses;

  geometry_msgs::Pose obj_pose;

  obj_pose.position.x = 0.230132;
  obj_pose.position.y = -0.194576;
  obj_pose.position.z = 1.1979;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = -0.0110219;
  obj_pose.position.y = -0.245896;
  obj_pose.position.z = 1.17472;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = 0.0914903;
  obj_pose.position.y = -0.0236473;
  obj_pose.position.z = 1.16408;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = -0.369081;
  obj_pose.position.y = -0.229498;
  obj_pose.position.z = 1.17214;
  object_poses.push_back(obj_pose);
  
  obj_pose.position.x = -0.209704;
  obj_pose.position.y = -0.329577;
  obj_pose.position.z = 1.19933;
  object_poses.push_back(obj_pose);
  
  obj_pose.position.x = 0.379415;
  obj_pose.position.y = -0.0289453;
  obj_pose.position.z = 1.16505;
  object_poses.push_back(obj_pose);
  
  obj_pose.position.x = -0.148887;
  obj_pose.position.y = -0.0324398;
  obj_pose.position.z = 1.13083;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = -0.224793;
  obj_pose.position.y = -0.185672;
  obj_pose.position.z = 1.16926;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = 0.408221;
  obj_pose.position.y = -0.350339;
  obj_pose.position.z = 1.22265;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = -0.34453;
  obj_pose.position.y = -0.0386084;
  obj_pose.position.z = 1.11656;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = 0.283352;
  obj_pose.position.y = -0.353287;
  obj_pose.position.z = 1.21362;
  object_poses.push_back(obj_pose);

  obj_pose.position.x = 0.172307;
  obj_pose.position.y = -0.354982;
  obj_pose.position.z = 1.22209;
  object_poses.push_back(obj_pose);

  // Transform the object poses to the robot base frame
  geometry_msgs::PoseStamped object_point;
  object_point.header.frame_id = "camera_rgb_optical_frame";
  object_point.header.stamp = ros::Time();

  std::vector<geometry_msgs::Pose> object_poses_new;
  geometry_msgs::PoseStamped temp_pose;

  for (int j = 0; j < object_poses.size(); j++){
    object_point.pose.position.x = object_poses[j].position.x;
    object_point.pose.position.y = object_poses[j].position.y;
    object_point.pose.position.z = object_poses[j].position.z;

    listener.transformPose("table_base_link", object_point, temp_pose);
    object_poses_new.push_back(temp_pose.pose);
  }

  const double jump_threshold = 0.0;
  const double eef_step = 0.01;
  const bool avoid_collisions = false;

  // Flag for physical execution on robot
  bool group_move = true;
  bool plan_v = false;

  // Offset params
  const float y_error = 0.09; //Add a little correction - was 0.09

  //Set starting tool position
  //tool_pose.position.x = 0.30; 
  //tool_pose.position.y = 0.51 - y_error; 
  //tool_pose.position.z = 0.2;
  //tool_pose.orientation.w = 1.0;
 
  geometry_msgs::PoseStamped current_pose = group.getCurrentPose();
  tool_pose = current_pose.pose;

  //group.setPoseTarget(tool_pose);
  //group.setGoalOrientationTolerance(0.1);

  // Now, we call the planner to compute the plan
  // and visualize it.
  // Note that we are just planning, not asking move_group 
  // to actually move the robot.
  //moveit::planning_interface::MoveGroup::Plan my_plan;

  //sleep(10.0); //Give some time to initialize everything before starting the planner

  //bool success = group.plan(my_plan);

  //ROS_INFO("Visualizing plan 1: Move above object (pose goal) %s",success?"":"FAILED");    
  // Sleep to give Rviz time to visualize the plan. 
  sleep(5.0);

  // Visualizing plans
  // ^^^^^^^^^^^^^^^^^
  // Now that we have a plan we can visualize it in Rviz.  This is not
  // necessary because the group.plan() call we made above did this
  // automatically.  But explicitly publishing plans is useful in cases that we
  // want to visualize a previously created plan.
  /*if (0)
  {
    ROS_INFO("Visualizing plan 1 (again)");    
    display_trajectory.trajectory_start = my_plan.start_state_;
    display_trajectory.trajectory.push_back(my_plan.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }*/

  //if (group_move)
  //  group.move();

  char wait_tool = ' ';

  while (wait_tool == ' '){
    ROS_INFO("Press any key when ready.. \n");
    wait_tool = getchar();
  }

  ROS_INFO("Attempting to close gripper.. \n");

  gripperGoal.position = gripper_close;
  gripperGoal.force = 100;

  gripperClient.sendGoal(gripperGoal);
  gripperClient.waitForResult(ros::Duration(10.0));
  if (!gripperClient.getResult()->success)
  {
    ROS_INFO("Closing gripper failed.");
    return 0;
  }

  ROS_INFO("Successfully closed gripper. \n");

  // Begin experiments
  std::vector<geometry_msgs::Pose> waypoints;
  moveit_msgs::RobotTrajectory trajectory;
  //moveit::planning_interface::MoveGroup::Plan my_plan;

  std::vector<int> results;
  std::ofstream my_file;

  my_file.open(output_filepath.c_str());

  float z_dist = 0.5;
  float centroid_offset = 0.0;

  for(int i = 0; i < object_poses_new.size(); i++){
    
    char key_press = ' ';
    ROS_INFO("Begin robot experiments \n");
    while (key_press == ' '){
      ROS_INFO("Press any key to begin \n");
      key_press = getchar();
    }

    geometry_msgs::Pose location = object_poses_new[i];
    int c = 10;

    location.position.z += z_dist;
    waypoints.push_back(location);
    location.position.z -= (z_dist - centroid_offset);
    waypoints.push_back(location);

    double fraction = group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory, avoid_collisions);
    if (fraction == 0.0){
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }
    
    my_plan.trajectory_ = trajectory;
    if (group_move)
      group.execute(my_plan);

    waypoints.clear();

    // Wait for user input on the outcome
    while (c > 1){
      c = getchar();
      if (c == 0 || c == 1){
        my_file << object_poses_new[i].position.x << object_poses_new[i].position.y << object_poses_new[i].position.z << c << "\n";
      } 
      else{
        ROS_INFO("Enter valid output, either 0 or 1 \n");
        c = 10;
      }
    }

    // Move back to starting position
    waypoints.push_back(tool_pose);
    fraction = group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory, avoid_collisions);
    if (fraction == 0.0){
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }
    
    my_plan.trajectory_ = trajectory;
    if (group_move)
      group.execute(my_plan);

    waypoints.clear();

  }

  my_file.close();

  return 0;
}