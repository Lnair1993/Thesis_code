# Install script for directory: /home/lnair3/Nimbus_ws/src/rail_manipulation_msgs

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/home/lnair3/Nimbus_ws/install")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/msg/Grasp.msg"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/msg/GraspingState.msg"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/msg/GraspFeedback.msg"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/msg/SegmentedObject.msg"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/msg/SegmentedObjectList.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/srv" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/srv/CallIK.srv"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/srv/CartesianPath.srv"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/srv/PairwiseRank.srv"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/srv/PrepareGrasp.srv"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/srv/SuggestGrasps.srv"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/action" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/Arm.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/Gripper.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/Lift.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/MoveToJointPose.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/MoveToPose.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/Pickup.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/Primitive.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/RecognizeObject.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/Store.action"
    "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/action/VerifyGrasp.action"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/ArmAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/ArmActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/ArmActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/ArmActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/ArmGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/ArmResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/ArmFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/GripperAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/GripperActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/GripperActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/GripperActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/GripperGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/GripperResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/GripperFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/LiftAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/LiftActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/LiftActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/LiftActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/LiftGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/LiftResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/LiftFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToJointPoseAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToJointPoseActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToJointPoseActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToJointPoseActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToJointPoseGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToJointPoseResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToJointPoseFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToPoseAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToPoseActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToPoseActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToPoseActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToPoseGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToPoseResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/MoveToPoseFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PickupAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PickupActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PickupActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PickupActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PickupGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PickupResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PickupFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PrimitiveAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PrimitiveActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PrimitiveActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PrimitiveActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PrimitiveGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PrimitiveResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/PrimitiveFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/RecognizeObjectAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/RecognizeObjectActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/RecognizeObjectActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/RecognizeObjectActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/RecognizeObjectGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/RecognizeObjectResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/RecognizeObjectFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/StoreAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/StoreActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/StoreActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/StoreActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/StoreGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/StoreResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/StoreFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/msg" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/VerifyGraspAction.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/VerifyGraspActionGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/VerifyGraspActionResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/VerifyGraspActionFeedback.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/VerifyGraspGoal.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/VerifyGraspResult.msg"
    "/home/lnair3/Nimbus_ws/devel/share/rail_manipulation_msgs/msg/VerifyGraspFeedback.msg"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/cmake" TYPE FILE FILES "/home/lnair3/Nimbus_ws/build/rail_manipulation_msgs/catkin_generated/installspace/rail_manipulation_msgs-msg-paths.cmake")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/lnair3/Nimbus_ws/devel/include/rail_manipulation_msgs")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/lnair3/Nimbus_ws/devel/share/roseus/ros/rail_manipulation_msgs")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/lnair3/Nimbus_ws/devel/share/common-lisp/ros/rail_manipulation_msgs")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  execute_process(COMMAND "/usr/bin/python" -m compileall "/home/lnair3/Nimbus_ws/devel/lib/python2.7/dist-packages/rail_manipulation_msgs")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/lnair3/Nimbus_ws/devel/lib/python2.7/dist-packages/rail_manipulation_msgs")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/lnair3/Nimbus_ws/build/rail_manipulation_msgs/catkin_generated/installspace/rail_manipulation_msgs.pc")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/cmake" TYPE FILE FILES "/home/lnair3/Nimbus_ws/build/rail_manipulation_msgs/catkin_generated/installspace/rail_manipulation_msgs-msg-extras.cmake")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs/cmake" TYPE FILE FILES
    "/home/lnair3/Nimbus_ws/build/rail_manipulation_msgs/catkin_generated/installspace/rail_manipulation_msgsConfig.cmake"
    "/home/lnair3/Nimbus_ws/build/rail_manipulation_msgs/catkin_generated/installspace/rail_manipulation_msgsConfig-version.cmake"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/rail_manipulation_msgs" TYPE FILE FILES "/home/lnair3/Nimbus_ws/src/rail_manipulation_msgs/package.xml")
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

