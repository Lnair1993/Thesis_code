#include <ros/ros.h>

#include <moveit/move_group_interface/move_group.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>

#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>

#include <rail_manipulation_msgs/GripperAction.h>
#include <actionlib/client/simple_action_client.h>
#include <rail_manipulation_msgs/LiftAction.h>

// Global Cartesian Planning params
//Distance to move for attaching objects

// (Optional) Create a publisher for visualizing plans in Rviz.

/*void pose_init(ros::NodeHandle node_handle, geometry_msgs::Pose &object1_pose, geometry_msgs::Pose &object2_pose, geometry_msgs::Pose &hammering_pose)
{
  // Display publisher
  display_publisher = node_handle.advertise<moveit_msgs::DisplayTrajectory>("/move_group/display_planned_path", 1, true);

  // Position of first part
  object1_pose.position.x = 0.30; 
  object1_pose.position.y = 0.51 - y_error; 
  object1_pose.position.z = 0.03; 

  // Position of second part
  object2_pose.orientation.w = 1.0;
  object2_pose.position.x = -0.2;
  object2_pose.position.y = 0.72 - y_error;
  object2_pose.position.z = 0.06;

  //Position of hammering object

}*/

/*void hammer_test(moveit::planning_interface::MoveGroup group, geometry_msgs::Pose hammering_pose)
{
  ROS_INFO("Testing Macgyvered object..");

  geometry_msgs::Pose hammering_pose;
  std::vector<geometry_msgs::Pose> waypoints;
  moveit_msgs::RobotTrajectory trajectory;
  moveit::planning_interface::MoveGroup::Plan my_plan;

  geometry_msgs::PoseStamped curr_pose = group.getCurrentPose();
  waypoints.push_back(curr_pose.pose); //Starting state

  hammering_pose.orientation.x = 0.198;
  hammering_pose.orientation.y = 0.208;
  hammering_pose.orientation.z = 0.684;
  hammering_pose.orientation.w = 0.671;

  hammering_pose.position.x = box_pose.position.x;
  hammering_pose.position.y = box_pose.position.y;
  hammering_pose.position.z = box_pose.position.z;
  waypoints.push_back(hammering_pose); // Hammering location and orientation

  hammering_pose.position.z = 0.8;
  waypoints.push_back(hammering_pose); // Lower hammer

  double fraction = group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory, avoid_collisions);

  if (fraction == 0.0)
  {
    ROS_INFO("Could not compute Cartesian path.");
    return 0;
  }

  my_plan.trajectory_ = trajectory;

  if (1)
  {
    ROS_INFO("Visualizing plan 9:Testing objects");  
    display_trajectory.trajectory.clear();  
    display_trajectory.trajectory_start = my_plan.start_state_;
    display_trajectory.trajectory.push_back(my_plan.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }

  if (group_move)
    group.execute(my_plan);  
}*/

int main(int argc, char **argv)
{
  ros::init(argc, argv, "nimbus_move");
  ros::NodeHandle node_handle;  
  ros::AsyncSpinner spinner(1);
  spinner.start();
  ROS_INFO("Initializing Move to Pose...");

  ros::Publisher display_publisher = node_handle.advertise<moveit_msgs::DisplayTrajectory>("/move_group/display_planned_path", 1, true);
  moveit_msgs::DisplayTrajectory display_trajectory;

  actionlib::SimpleActionClient<rail_manipulation_msgs::GripperAction> gripperClient("gripper_actions/gripper_manipulation");
  rail_manipulation_msgs::GripperGoal gripperGoal;
  
  //actionlib::SimpleActionClient<robotiq_85_msgs::GripperCmd> gripperClient("gripper_actions/cmd");
  //robotiq_85_msgs::GripperCmd gripperGoal;
  

  /* This sleep is ONLY to allow Rviz to come up */
  sleep(5.0);
  
  // The group being controlled
  moveit::planning_interface::MoveGroup group("arm"); //gripper or arm
  moveit::planning_interface::PlanningSceneInterface planning_scene_interface;  

  // We can print the name of the reference frame and end-effector for this robot.
  ROS_INFO("Reference frame: %s", group.getPlanningFrame().c_str());
  ROS_INFO("End-effector link: %s", group.getEndEffectorLink().c_str());

  // Initialize object positions
  geometry_msgs::Pose target_pose1, goal_pose;

  const double jump_threshold = 0.0;
  const double eef_step = 0.01;
  const bool avoid_collisions = false;

  // Flag for physical execution on robot
  bool group_move = true;
  bool hammer = false;
  bool scoop = true;
  bool spatula = false;
  bool plan_v = true;

  // Offset params
  const float y_error = 0.09; //Add a little correction - was 0.09
  const float z_dist = 0.15;
  const float attach_dist = 0.08; //Was 0.05 -> 0.08 

  int gripper_orientation = 1; //1 - width, 0 - length

  /* Point cloud poses in table_base_link:
  InputCloud0 - [0.3, 0.51, 0.03]
  InputCloud1 - [-0.2, 0.72, 0.06]
  InputCloud2 - 
  InputCloud3 - [-0.2, 0.51, 0.04]
  */

  //Trying to get gripper orientation
  goal_pose.orientation.w = 1.0;
  goal_pose.position.x = -0.2;
  goal_pose.position.y = 0.72;
  goal_pose.position.z = 0.06;

  target_pose1.position.x = 0.30; 
  target_pose1.position.y = 0.51 - y_error; 
  target_pose1.position.z = 0.03 + z_dist;

  if (gripper_orientation) // Orient gripper along shorter side of table (width)
  {
    target_pose1.orientation.x = 0.489; 
    target_pose1.orientation.y = 0.522;
    target_pose1.orientation.z = -0.489;
    target_pose1.orientation.w = 0.5;
  }
  else // Orient gripper along longer side of the table (length)
  {
    target_pose1.orientation.x = -0.006; 
    target_pose1.orientation.y = 0.704;
    target_pose1.orientation.z = -0.015;
    target_pose1.orientation.w = 0.71;
  }
 
  group.setPoseTarget(target_pose1);
  group.setGoalOrientationTolerance(0.1);

  // Now, we call the planner to compute the plan
  // and visualize it.
  // Note that we are just planning, not asking move_group 
  // to actually move the robot.
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

  if (group_move)
    group.move();
  
  //******************************************************
  // Second phase of the plan - lower the hand down
  //sleep(5.0);
  ROS_INFO("Starting phase 2 of planning: Lowering gripper..");

  //robot_state::RobotState start_state(*group.getCurrentState());
  //const robot_state::JointModelGroup *joint_model_group = start_state.getJointModelGroup(group.getName());
  //start_state.setFromIK(joint_model_group, target_pose1);
  //group.setStartState(start_state);

  std::vector<geometry_msgs::Pose> waypoints;
  waypoints.push_back(target_pose1);

  target_pose1.position.z = 0.058;
  waypoints.push_back(target_pose1);

  moveit_msgs::RobotTrajectory trajectory;

  double fraction = group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory, avoid_collisions);

  if (fraction == 0.0)
  {
    ROS_INFO("Could not compute Cartesian path.");
    return 0;
  }

  ROS_INFO("Lowering arm..");

  //target_pose1.position.z = 0.058; //Lower the arm 
  //group.setPoseTarget(target_pose1);

  //group.setGoalOrientationTolerance(0.1);


  // Now, we call the planner to compute the plan
  // and visualize it.
  // Note that we are just planning, not asking move_group 
  // to actually move the robot.
  moveit::planning_interface::MoveGroup::Plan my_plan2;
  my_plan2.trajectory_ = trajectory;

  //success = group.plan(my_plan2);

  //ROS_INFO("Visualizing plan 2: Lower arm %s",success?"":"FAILED");    
  // Sleep to give Rviz time to visualize the plan. 
  //sleep(5.0);

  // Visualizing plans
  // ^^^^^^^^^^^^^^^^^
  // Now that we have a plan we can visualize it in Rviz.  This is not
  // necessary because the group.plan() call we made above did this
  // automatically.  But explicitly publishing plans is useful in cases that we
  // want to visualize a previously created plan.
  if (plan_v)
  {
    ROS_INFO("Visualizing plan 2: Lower arm");    
    display_trajectory.trajectory.clear();
    display_trajectory.trajectory_start = my_plan2.start_state_;
    display_trajectory.trajectory.push_back(my_plan2.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }

  // Moving to a pose goal
  // ^^^^^^^^^^^^^^^^^^^^^
  //
  // Moving to a pose goal is similar to the step above
  // except we now use the move() function. Note that
  // the pose goal we had set earlier is still active 
  // and so the robot will try to move to that goal. We will
  // not use that function in this tutorial since it is 
  // a blocking function and requires a controller to be active
  // and report success on execution of a trajectory.
 
  // Uncomment below line when working with a real robot
  if (group_move)
    group.execute(my_plan2);
    //group.move();

  //Gripper open action
  /*ROS_INFO("Attempting to open gripper..");
  gripperGoal.close = false;
  gripperClient.sendGoal(gripperGoal); 
  gripperClient.waitForResult(ros::Duration(10.0));
  if (!gripperClient.getResult()->success)
  {
    ROS_INFO("Opening gripper failed.");
    return 0;
  }

  ROS_INFO("Successfully opened gripper.");*/

  //Gripper close action
  ROS_INFO("Attempting to close gripper..");
  //gripperGoal.close = true;
  //gripperGoal.force = 50; //Was 155

  gripperGoal.position = 0.0;
  gripperGoal.force = 155;

  gripperClient.sendGoal(gripperGoal);
  gripperClient.waitForResult(ros::Duration(10.0));
  if (!gripperClient.getResult()->success)
  {
    ROS_INFO("Closing gripper failed.");
    return 0;
  }

  ROS_INFO("Successfully closed gripper.");

  //TO DO: Verify that gripper is holding object
  //rail_manipulation_msgs::VerifyGraspGoal verifyGoal;

  //MOVE TO GOAL OBJECT ********************************************************************
  sleep(5.0);
  //return 0;

  //USING WAYPOINTS FOR REST OF THE STUFF ***************************************************

  std::vector<geometry_msgs::Pose> waypoints2;
  moveit::planning_interface::MoveGroup::Plan my_plan3;

  waypoints2.push_back(target_pose1); //Starting state - object gripped

  target_pose1.position.z = 0.25; //Lift object
  waypoints2.push_back(target_pose1);

  fraction = group.computeCartesianPath(waypoints2, eef_step, jump_threshold, trajectory, avoid_collisions);

  if (fraction == 0.0)
  {
    ROS_INFO("Could not compute Cartesian path.");
    return 0;
  }

  ROS_INFO("Lifting arm..");

  my_plan3.trajectory_ = trajectory;

  if (plan_v)
  {
    ROS_INFO("Visualizing plan 3: Lifting object");   
    display_trajectory.trajectory.clear(); 
    display_trajectory.trajectory_start = my_plan3.start_state_;
    display_trajectory.trajectory.push_back(my_plan3.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }


  if (group_move)
    group.execute(my_plan3);

  /*robot_state::RobotState start_state2(*group.getCurrentState());
  const robot_state::JointModelGroup *joint_model_group2 = start_state2.getJointModelGroup(group.getName());
  start_state2.setFromIK(joint_model_group2, target_pose1);
  group.setStartState(start_state2);

  target_pose1.position.x = 0.0;
  target_pose1.position.y = goal_pose.position.y - y_error; //Move to center of workspace - using planner for this
  waypoints2.push_back(target_pose1);

  group.setPoseTarget(target_pose1);
  success = group.plan(my_plan3);

  ROS_INFO("Visualizing plan 4: Move grasped object %s",success?"":"FAILED");    
  // Sleep to give Rviz time to visualize the plan.
  sleep(5.0);*/

  // EXPLORATION PART ------ -------
  // ^^^^^^^^^^^^^^^^

  /*std::vector<geometry_msgs::Pose> waypoints_ex;
  waypoints_ex.push_back(target_pose1); //Starting pose

  target_pose1.position.x = goal_pose.position.x + 0.8*goal_pose.position.x; //goal_pose + 0.75*goal_pose for hammer
  target_pose1.position.y = goal_pose.position.y - y_error;
  waypoints_ex.push_back(target_pose1); //Move to other side of object

  target_pose1.position.z = 0.058; //Lower object
  waypoints_ex.push_back(target_pose1);

  target_pose1.position.x += attach_dist; //Attach objects
  waypoints_ex.push_back(target_pose1);

  fraction = group.computeCartesianPath(waypoints_ex, eef_step, jump_threshold, trajectory, avoid_collisions);

  if (fraction == 0.0)
  {
    ROS_INFO("Could not compute Cartesian path.");
    return 0;
  }

  ROS_INFO("Attaching objects..");

  my_plan3.trajectory_ = trajectory;

  if (1)
  {
    ROS_INFO("Visualizing plan 5: Exploration 1");  
    display_trajectory.trajectory.clear();  
    display_trajectory.trajectory_start = my_plan3.start_state_;
    display_trajectory.trajectory.push_back(my_plan3.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }

  if (group_move)
    group.execute(my_plan3);

  waypoints_ex.clear();
  waypoints_ex.push_back(target_pose1);
  target_pose1.position.z = 0.25; //Lift objects
  waypoints_ex.push_back(target_pose1);

  fraction = group.computeCartesianPath(waypoints_ex, eef_step, jump_threshold, trajectory, avoid_collisions);

  if (fraction == 0.0)
  {
    ROS_INFO("Could not compute Cartesian path.");
    return 0;
  }

  ROS_INFO("Attaching objects..");

  my_plan3.trajectory_ = trajectory;

  if (1)
  {
    ROS_INFO("Visualizing plan 5: Exploration 2");  
    display_trajectory.trajectory.clear();  
    display_trajectory.trajectory_start = my_plan3.start_state_;
    display_trajectory.trajectory.push_back(my_plan3.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }

  if (group_move)
    group.execute(my_plan3);*/

  // ORIGINAL PART
  // ^^^^^^^^^^^^^

  std::vector<geometry_msgs::Pose> waypoints3;
  waypoints3.push_back(target_pose1); //Starting state

  target_pose1.position.x = 0.0;
  target_pose1.position.y = goal_pose.position.y - y_error; //Move to center of workspace
  waypoints3.push_back(target_pose1);

  target_pose1.position.z = 0.058; //Lower object
  waypoints3.push_back(target_pose1);

  target_pose1.position.x -= attach_dist; //Attach object
  waypoints3.push_back(target_pose1);

  fraction = group.computeCartesianPath(waypoints3, eef_step, jump_threshold, trajectory, avoid_collisions);

  if (fraction == 0.0)
  {
    ROS_INFO("Could not compute Cartesian path.");
    return 0;
  }

  ROS_INFO("Attaching objects..");

  my_plan3.trajectory_ = trajectory;

  if (plan_v)
  {
    ROS_INFO("Visualizing plan 5: Attaching objects");  
    display_trajectory.trajectory.clear();  
    display_trajectory.trajectory_start = my_plan3.start_state_;
    display_trajectory.trajectory.push_back(my_plan3.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }


  if (group_move)
    group.execute(my_plan3);

  // ^^^^^^^^^^^^^^^^^

  waypoints3.clear();
  waypoints3.push_back(target_pose1); //Starting pose

  target_pose1.position.z = 0.25;
  waypoints3.push_back(target_pose1); //Lift object

  fraction = group.computeCartesianPath(waypoints3, eef_step, jump_threshold, trajectory, avoid_collisions);

  if (fraction == 0.0)
  {
    ROS_INFO("Could not compute Cartesian path.");
    return 0;
  }

  ROS_INFO("Attaching objects..");

  my_plan3.trajectory_ = trajectory;

  if (plan_v)
  {
    ROS_INFO("Visualizing plan 5: Attaching objects");  
    display_trajectory.trajectory.clear();  
    display_trajectory.trajectory_start = my_plan3.start_state_;
    display_trajectory.trajectory.push_back(my_plan3.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }


  if (group_move)
    group.execute(my_plan3);

  //TEST NEW OBJECT
  //REMOVE THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  //return 0; 

  //*****************************************************************************************
  
  /*ROS_INFO("Starting phase 3 of planning: Moving grasped object..");

  //robot_state::RobotState start_state2(*group.getCurrentState());
  //const robot_state::JointModelGroup *joint_model_group2 = start_state2.getJointModelGroup(group.getName());
  //start_state2.setFromIK(joint_model_group2, target_pose1);
  //group.setStartState(start_state2);

  target_pose1.position.z = 0.25; //Lower the arm 
  group.setPoseTarget(target_pose1);

  moveit::planning_interface::MoveGroup::Plan my_plan3;

  success = group.plan(my_plan3);

  ROS_INFO("Visualizing plan 3: Move grasped object %s",success?"":"FAILED");    
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
    ROS_INFO("Visualizing plan 3 (again)");    
    display_trajectory.trajectory_start = my_plan.start_state_;
    display_trajectory.trajectory.push_back(my_plan.trajectory_);
    display_publisher.publish(display_trajectory);
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
  }

  if (group_move)
    group.move();


  //********************* OBJECT SHOULD BE GRASPED AT THIS POINT *******************************

  // Move gripper to goal_pose, with x = 0
  // Lower gripper to target pose z
  // Move gripper to goal_pose original x

  ROS_INFO("Moving the grasp part to object part..");

  geometry_msgs::Pose waypoint1, waypoint2, waypoint3;

  //Move to center
  waypoint1.orientation.x = target_pose1.orientation.x; 
  waypoint1.orientation.y = target_pose1.orientation.y;
  waypoint1.orientation.z = target_pose1.orientation.z;
  waypoint1.orientation.w = target_pose1.orientation.w;
  waypoint1.position.x = 0.0;
  waypoint1.position.y = goal_pose.position.y-y_error;
  waypoint1.position.z = target_pose1.position.z;

  //Lower object
  waypoint2.orientation.x = target_pose1.orientation.x; 
  waypoint2.orientation.y = target_pose1.orientation.y;
  waypoint2.orientation.z = target_pose1.orientation.z;
  waypoint2.orientation.w = target_pose1.orientation.w;
  waypoint2.position.x = 0.0;
  waypoint2.position.y = goal_pose.position.y-y_error; //waypoint1.position.y;
  waypoint2.position.z = goal_pose.position.z+0.01;

  //Attach objects
  waypoint3.orientation.x = target_pose1.orientation.x; 
  waypoint3.orientation.y = target_pose1.orientation.y;
  waypoint3.orientation.z = target_pose1.orientation.z;
  waypoint3.orientation.w = target_pose1.orientation.w;
  waypoint3.position.x = waypoint2.position.x-0.1;
  waypoint3.position.y = waypoint2.position.y;
  waypoint3.position.z = waypoint2.position.z;

  moveit::planning_interface::MoveGroup::Plan my_plan4;

  group.setPoseTarget(waypoint1);
  bool success2 = group.plan(my_plan4);

  ROS_INFO("Visualizing plan 4: Move grasped object to workspace center %s",success?"":"FAILED");    
  // Sleep to give Rviz time to visualize the plan.
  sleep(5.0);

  //group.move();

  ROS_INFO("Lowering object..");
  robot_state::RobotState start_state3(*group.getCurrentState());
  const robot_state::JointModelGroup *joint_model_group3 = start_state3.getJointModelGroup(group.getName());
  start_state3.setFromIK(joint_model_group3, waypoint1);
  group.setStartState(start_state3);

  group.setPoseTarget(waypoint2);
  success2 = group.plan(my_plan4);

  ROS_INFO("Visualizing plan 5: Lower grasped object to workspace %s",success?"":"FAILED");    
  // Sleep to give Rviz time to visualize the plan.
  sleep(5.0);

  if (group_move)
    group.move();

  ROS_INFO("Attaching objects..");
  robot_state::RobotState start_state4(*group.getCurrentState());
  const robot_state::JointModelGroup *joint_model_group4 = start_state4.getJointModelGroup(group.getName());
  start_state4.setFromIK(joint_model_group4, waypoint2);
  group.setStartState(start_state4);

  group.setPoseTarget(waypoint3);
  success2 = group.plan(my_plan4);

  ROS_INFO("Visualizing plan 6: Attach objects %s",success?"":"FAILED");    
  // Sleep to give Rviz time to visualize the plan.
  sleep(5.0);

  if (group_move)
    group.move();*/

  if (hammer)
  {

  //***************************************************************************
  //RAISE THE OBJECT

    geometry_msgs::Pose mgPose, hammering_pose;
    std::vector<geometry_msgs::Pose> waypoints_test;

    mgPose.orientation.x = -0.157;
    mgPose.orientation.y = -0.681;
    mgPose.orientation.z = 0.497;
    mgPose.orientation.w = 0.514;

    mgPose.position.x = -0.067;
    mgPose.position.y = 0.568;
    mgPose.position.z = 0.369; 


    hammering_pose.orientation.x = 0.198;
    hammering_pose.orientation.y = 0.208;
    hammering_pose.orientation.z = 0.684;
    hammering_pose.orientation.w = 0.671;

    hammering_pose.position.x = 0.505;
    hammering_pose.position.y = 0.341;
    hammering_pose.position.z = 0.390;

    //group.setPoseTarget(hammering_pose);
    //group.setGoalOrientationTolerance(0.1);

    //moveit::planning_interface::MoveGroup::Plan my_plan_final;

    //success = group.plan(my_plan_final);

    //ROS_INFO("Visualizing plan: Move to testing location %s",success?"":"FAILED");    
    // Sleep to give Rviz time to visualize the plan. 
    //sleep(5.0);
    //group.move();

    waypoints_test.push_back(target_pose1); // Starting pose
    waypoints_test.push_back(hammering_pose); // Hammering location and orientation

    hammering_pose.position.z = 0.29;
    waypoints_test.push_back(hammering_pose); // Lower hammer

    fraction = group.computeCartesianPath(waypoints_test, eef_step, jump_threshold, trajectory, true);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    my_plan.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 9:Testing objects");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan.start_state_;
      display_trajectory.trajectory.push_back(my_plan.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan); 

    //sleep(6.0);   

    //return 0;

    /*ROS_INFO("Raising Macgyvered object..");
    robot_state::RobotState start_state5(*group.getCurrentState());
    const robot_state::JointModelGroup *joint_model_group5 = start_state5.getJointModelGroup(group.getName());
    start_state5.setFromIK(joint_model_group5, target_pose1);
    group.setStartState(start_state5);

    group.setPoseTarget(mgPose);
    success = group.plan(my_plan3);

    ROS_INFO("Visualizing plan 7: Raising the Macgyvered object %s",success?"":"FAILED");    
    // Sleep to give Rviz time to visualize the plan.
    sleep(5.0);

    if (group_move)
      group.move();

    //FOR HAMMERING ************************************************************************************
    
    //Change gripper orientation
    //Move down
    //Move up 


    //Assuming the hammer broke here ************************************
    // 1) Give sleep time for me to remove end of hammer if it didn't
    // Retrieve current pose of the arm
    // Move from current pose to original orientation
    // Move to pose of better object part, but x = 0.0, z = 0.25, y = original_y - y_error;
    // Move towards the better piece
    // Repeat above test -- Hopefully hammer stays intact

    sleep(5.0); //To remove the end part if it didn't fall off*/


    //MOVING TO NEW PART *******************************************************************
    std::vector<geometry_msgs::Pose> waypoints5, waypoints6;

    geometry_msgs::Pose goal_better = target_pose1;
    geometry_msgs::Pose goal_temp;

    goal_better.position.x = -0.2;
    goal_better.position.y = 0.51 - y_error;
    goal_better.position.z = 0.04;

    geometry_msgs::PoseStamped curr_pose = group.getCurrentPose();
    waypoints5.push_back(curr_pose.pose); //Start state

    goal_temp = curr_pose.pose;
    goal_temp.position.z += z_dist; //Raise arm to check if object attached
    waypoints5.push_back(goal_temp);

    target_pose1.position.x = 0.0;
    target_pose1.position.y = goal_better.position.y;
    target_pose1.position.z = goal_better.position.z + z_dist; //Move closer to next part
    waypoints5.push_back(target_pose1);

    fraction = group.computeCartesianPath(waypoints5, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Making new object..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Moving to new part");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

    waypoints6.push_back(target_pose1); //Start state

    target_pose1.position.z = 0.058;
    waypoints6.push_back(target_pose1); //Lower object

    target_pose1.position.x -= (attach_dist+0.02);
    waypoints6.push_back(target_pose1); //Attach objects

    fraction = group.computeCartesianPath(waypoints6, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Making new object..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 11:Attaching new parts");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);


    //NEED TO TEST THIS PART COMBO
    hammering_pose.orientation.x = 0.997; //0.167;
    hammering_pose.orientation.y = -0.072; //0.27;
    hammering_pose.orientation.z = -0.017; //0.502;
    hammering_pose.orientation.w = 0.016; //0.805;

    hammering_pose.position.x = 0.505; //0.52;
    hammering_pose.position.y = 0.341; //0.411;
    hammering_pose.position.z = 0.39;

    /*group.setPoseTarget(hammering_pose);
    group.setGoalOrientationTolerance(0.1);

    success = group.plan(my_plan_final);

    ROS_INFO("Visualizing plan: Move to testing location %s",success?"":"FAILED");    
    // Sleep to give Rviz time to visualize the plan. 
    sleep(5.0);
    group.move();*/


    std::vector<geometry_msgs::Pose> waypoints_newtest;
    waypoints_newtest.push_back(target_pose1); // Starting pose
    waypoints_newtest.push_back(hammering_pose); // Hammering location and orientation

    hammering_pose.position.z = 0.22;
    waypoints_newtest.push_back(hammering_pose); // Lower hammer

    fraction = group.computeCartesianPath(waypoints_newtest, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    my_plan.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 9:Testing objects");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan.start_state_;
      display_trajectory.trajectory.push_back(my_plan.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan);

    //CHECK THAT NEW PART ATTACHED

    std::vector<geometry_msgs::Pose> waypoints7;

    curr_pose = group.getCurrentPose();
    waypoints7.push_back(curr_pose.pose); //Start state

    goal_temp = curr_pose.pose;
    goal_temp.position.z += z_dist; //Raise arm to check if object attached
    waypoints7.push_back(goal_temp);

    target_pose1.position.x = 0.0;
    target_pose1.position.y = goal_better.position.y;
    target_pose1.position.z = goal_better.position.z + z_dist; //Move closer to next part
    waypoints7.push_back(target_pose1);

    fraction = group.computeCartesianPath(waypoints7, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Making new object..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Moving to new part");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);
} //If hammering task

else if(scoop)
{
    //MOVING TO NEW PART *******************************************************************
    /*std::vector<geometry_msgs::Pose> waypoints5, waypoints6;

    geometry_msgs::Pose goal_better = target_pose1;
    geometry_msgs::Pose goal_temp;

    goal_better.position.x = -0.2;
    goal_better.position.y = 0.51 - y_error;
    goal_better.position.z = 0.04;

    geometry_msgs::PoseStamped curr_pose = group.getCurrentPose();
    waypoints5.push_back(curr_pose.pose); //Start state

    goal_temp = curr_pose.pose;
    goal_temp.position.z += z_dist; //Raise arm to check if object attached
    waypoints5.push_back(goal_temp);

    target_pose1.position.x = 0.0;
    target_pose1.position.y = goal_better.position.y;
    target_pose1.position.z = goal_better.position.z + z_dist; //Move closer to next part
    waypoints5.push_back(target_pose1);

    fraction = group.computeCartesianPath(waypoints5, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Making new object..");

    my_plan3.trajectory_ = trajectory;

    if (1)
    {
      ROS_INFO("Visualizing plan 10: Moving to new part");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

    waypoints6.push_back(target_pose1); //Start state

    target_pose1.position.z = 0.058;
    waypoints6.push_back(target_pose1); //Lower object

    target_pose1.position.x -= attach_dist;
    waypoints6.push_back(target_pose1); //Attach objects

    fraction = group.computeCartesianPath(waypoints6, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Making new object..");

    my_plan3.trajectory_ = trajectory;

    if (1)
    {
      ROS_INFO("Visualizing plan 11:Attaching new parts");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);*/

  // SCOOPING TASK ******************************************************************************************
  // ^^^^^^^^^^^^^
  //Move above bowl - same as hammer location
  //Tilt arm gripper
  //Lower to bowl
  //Move a little horizontal to scoop
  //Tilt arm gripper
  //Lift

  geometry_msgs::Pose scoop_pose;
  std::vector<geometry_msgs::Pose> scoop_waypoints;

  scoop_pose.position.x = 0.676;
  scoop_pose.position.y = 0.4;
  scoop_pose.position.z = 0.278;

  scoop_pose.orientation.x = 0.61; //0.681; //0.61; //NEED TO TILT GRIPPER LESSER!!!!!! ******************************* !!!!!!!
  scoop_pose.orientation.y = 0.21; //0.252; //0.21;
  scoop_pose.orientation.z = -0.144; //-0.274; //-0.144;
  scoop_pose.orientation.w = 0.75; //0.63; //0.75;

  scoop_waypoints.push_back(target_pose1); //Starting state

  target_pose1 = scoop_pose;

  scoop_waypoints.push_back(target_pose1);

  target_pose1.position.z = 0.18; //Was 0.18

  scoop_waypoints.push_back(target_pose1); //Lower the scoop

  fraction = group.computeCartesianPath(scoop_waypoints, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Scooping..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Scooping");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

  scoop_waypoints.clear();
  scoop_waypoints.push_back(target_pose1);

  target_pose1.position.x -= 0.1;
  scoop_waypoints.push_back(target_pose1); //Scoop

  target_pose1.orientation.x = 0.444; //0.606; //0.444;
  target_pose1.orientation.y = 0.538; //0.264; //0.538;
  target_pose1.orientation.z = -0.44; //-0.341; //-0.44;
  target_pose1.orientation.w = 0.565; //0.668; //0.565;

  //scoop_waypoints.push_back(target_pose1);

  target_pose1.position.z = 0.25;
  scoop_waypoints.push_back(target_pose1); //Lift scoop

  fraction = group.computeCartesianPath(scoop_waypoints, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Scooping..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Scooping");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

  scoop_waypoints.clear();
  scoop_waypoints.push_back(target_pose1); //Starting pose

  target_pose1.position.x = 0.0;
  target_pose1.position.y = 0.51;
  target_pose1.position.z = 0.25;

  scoop_waypoints.push_back(target_pose1); //Move to center for view

  fraction = group.computeCartesianPath(scoop_waypoints, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Scooping..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Scooping");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

}

else if(spatula)
{
	// SPATULA TASK
	// ^^^^^^^^^^^^

	// Drop object back
	geometry_msgs::Pose drop_loc;
	drop_loc.position.x = 0.30;
	drop_loc.position.y = 0.51 - y_error;
	drop_loc.position.z = 0.03 + z_dist/2;

	drop_loc.orientation.x = 0.489;
	drop_loc.orientation.y = 0.522;
	drop_loc.orientation.z = -0.489;
	drop_loc.orientation.w = 0.5;

	std::vector<geometry_msgs::Pose> new_wp;
	new_wp.push_back(target_pose1); // Starting state

	target_pose1 = drop_loc;
	new_wp.push_back(drop_loc); // Drop first object

	fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Dropping objects..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Drop object");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

	//Gripper open action
  	ROS_INFO("Attempting to open gripper..");
  	//gripperGoal.close = false;
  	gripperGoal.position = 100.0;
  	gripperClient.sendGoal(gripperGoal); 
  	gripperClient.waitForResult(ros::Duration(10.0));
  	if (!gripperClient.getResult()->success)
  	{
    	ROS_INFO("Opening gripper failed.");
    	return 0;
  	}

  	ROS_INFO("Successfully opened gripper.");

	//Pick up object 2
  	new_wp.clear();

  	new_wp.push_back(target_pose1); //Starting state

  	target_pose1.position.x = -0.2 - 0.05;
    target_pose1.position.y = 0.51 - y_error;
    target_pose1.position.z = 0.06 + z_dist;
	
    new_wp.push_back(target_pose1); //Move to new location

    target_pose1.position.z = 0.09;
    new_wp.push_back(target_pose1); //Lower gripper

    fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Choosing new object..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Pick new object");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

  	//Gripper close action
  	ROS_INFO("Attempting to close gripper..");
  	//gripperGoal.close = true;
  	gripperGoal.position = 0.0;
  	gripperGoal.force = 150; //Was 155
  	gripperClient.sendGoal(gripperGoal);
  	gripperClient.waitForResult(ros::Duration(10.0));
  	if (!gripperClient.getResult()->success)
  	{
    	ROS_INFO("Closing gripper failed.");
    	return 0;
  	}

  	ROS_INFO("Successfully closed gripper.");

	//Move to target

  	new_wp.clear();

  	new_wp.push_back(target_pose1); //Starting state

	target_pose1.position.x = -0.2-0.02;
    target_pose1.position.y = 0.72 - y_error;
    target_pose1.position.z = 0.06 + z_dist;

    new_wp.push_back(target_pose1); //Spatula location

    fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Choosing new object..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Pick new object");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

  	new_wp.clear();
  	new_wp.push_back(target_pose1); // Starting state

    target_pose1.position.z = 0.095; //Lower handle
    new_wp.push_back(target_pose1);

    fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Lower handle..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Lower handle");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);
	
	//Lift tool
  	new_wp.clear();
  	new_wp.push_back(target_pose1); //Starting state

  	target_pose1.position.z = target_pose1.position.z + z_dist;
  	new_wp.push_back(target_pose1); // Lift tool

  	fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Lift new tool..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Lifting tool");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);


  	// Spatula with tool
  	geometry_msgs::Pose spatula_pose;
  	spatula_pose.position.x = 0.605;
  	spatula_pose.position.y = 0.28;
  	spatula_pose.position.z = 0.112;

  	spatula_pose.orientation.x = 0.708;
  	spatula_pose.orientation.y = -0.001;
  	spatula_pose.orientation.z = -0.706;
  	spatula_pose.orientation.w = 0.008;

  	new_wp.clear();
  	new_wp.push_back(target_pose1);

  	target_pose1 = spatula_pose;
  	new_wp.push_back(target_pose1);

  	fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Preparing to spatula..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Preparing spatula pose");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

  	new_wp.clear();
  	new_wp.push_back(target_pose1); //Starting state

  	target_pose1.position.y = target_pose1.position.y + 0.1; //Move spatula forward
  	new_wp.push_back(target_pose1);

  	fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Spatula lettuce..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Spatula lettuce");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

  	new_wp.clear();
  	new_wp.push_back(target_pose1); //Starting state

  	target_pose1.position.z = target_pose1.position.z + z_dist; //Lift object
  	new_wp.push_back(target_pose1);

  	fraction = group.computeCartesianPath(new_wp, eef_step, jump_threshold, trajectory, avoid_collisions);

    if (fraction == 0.0)
    {
      ROS_INFO("Could not compute Cartesian path.");
      return 0;
    }

    ROS_INFO("Lift lettuce..");

    my_plan3.trajectory_ = trajectory;

    if (plan_v)
    {
      ROS_INFO("Visualizing plan 10: Lift lettuce");  
      display_trajectory.trajectory.clear();  
      display_trajectory.trajectory_start = my_plan3.start_state_;
      display_trajectory.trajectory.push_back(my_plan3.trajectory_);
      display_publisher.publish(display_trajectory);
      // Sleep to give Rviz time to visualize the plan. 
      sleep(5.0);
    }

    if (group_move)
      group.execute(my_plan3);

}

return 0;
}