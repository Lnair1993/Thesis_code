cmake_minimum_required(VERSION 2.8.3)
project(nimbus_explore)

find_package(catkin REQUIRED
  COMPONENTS
    actionlib
    control_msgs
    ecl_geometry
    message_generation
    geometry_msgs
    pcl_conversions
    pcl_ros
    rail_manipulation_msgs
    sensor_msgs
    std_srvs
    tf
    tf2_ros    
    roscpp
    std_msgs
    genmsg
    moveit_core
    moveit_ros_planning
    moveit_ros_planning_interface
    pluginlib
    cmake_modules
    geometric_shapes
)

find_package(Boost REQUIRED system filesystem date_time thread)

catkin_package(
  CATKIN_DEPENDS
    moveit_core
    moveit_ros_planning_interface
    interactive_markers
)
find_package(Eigen REQUIRED)

###########
## Build ##
###########

include_directories(SYSTEM ${Boost_INCLUDE_DIR} ${EIGEN_INCLUDE_DIRS})
include_directories(${catkin_INCLUDE_DIRS})

link_directories(${catkin_LIBRARY_DIRS})

add_executable(nimbus_explore src/nimbus_explore.cpp)
target_link_libraries(nimbus_explore ${catkin_LIBRARIES})


