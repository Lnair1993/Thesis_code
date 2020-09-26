;; Auto-generated. Do not edit!


(when (boundp 'rail_manipulation_msgs::PairwiseRank)
  (if (not (find-package "RAIL_MANIPULATION_MSGS"))
    (make-package "RAIL_MANIPULATION_MSGS"))
  (shadow 'PairwiseRank (find-package "RAIL_MANIPULATION_MSGS")))
(unless (find-package "RAIL_MANIPULATION_MSGS::PAIRWISERANK")
  (make-package "RAIL_MANIPULATION_MSGS::PAIRWISERANK"))
(unless (find-package "RAIL_MANIPULATION_MSGS::PAIRWISERANKREQUEST")
  (make-package "RAIL_MANIPULATION_MSGS::PAIRWISERANKREQUEST"))
(unless (find-package "RAIL_MANIPULATION_MSGS::PAIRWISERANKRESPONSE")
  (make-package "RAIL_MANIPULATION_MSGS::PAIRWISERANKRESPONSE"))

(in-package "ROS")



(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))


(defclass rail_manipulation_msgs::PairwiseRankRequest
  :super ros::object
  :slots ())

(defmethod rail_manipulation_msgs::PairwiseRankRequest
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass rail_manipulation_msgs::PairwiseRankResponse
  :super ros::object
  :slots (_grasp_list ))

(defmethod rail_manipulation_msgs::PairwiseRankResponse
  (:init
   (&key
    ((:grasp_list __grasp_list) (instance geometry_msgs::PoseArray :init))
    )
   (send-super :init)
   (setq _grasp_list __grasp_list)
   self)
  (:grasp_list
   (&rest __grasp_list)
   (if (keywordp (car __grasp_list))
       (send* _grasp_list __grasp_list)
     (progn
       (if __grasp_list (setq _grasp_list (car __grasp_list)))
       _grasp_list)))
  (:serialization-length
   ()
   (+
    ;; geometry_msgs/PoseArray _grasp_list
    (send _grasp_list :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; geometry_msgs/PoseArray _grasp_list
       (send _grasp_list :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; geometry_msgs/PoseArray _grasp_list
     (send _grasp_list :deserialize buf ptr-) (incf ptr- (send _grasp_list :serialization-length))
   ;;
   self)
  )

(defclass rail_manipulation_msgs::PairwiseRank
  :super ros::object
  :slots ())

(setf (get rail_manipulation_msgs::PairwiseRank :md5sum-) "6c2ebd2e566677f8b421547f8e5266ee")
(setf (get rail_manipulation_msgs::PairwiseRank :datatype-) "rail_manipulation_msgs/PairwiseRank")
(setf (get rail_manipulation_msgs::PairwiseRank :request) rail_manipulation_msgs::PairwiseRankRequest)
(setf (get rail_manipulation_msgs::PairwiseRank :response) rail_manipulation_msgs::PairwiseRankResponse)

(defmethod rail_manipulation_msgs::PairwiseRankRequest
  (:response () (instance rail_manipulation_msgs::PairwiseRankResponse :init)))

(setf (get rail_manipulation_msgs::PairwiseRankRequest :md5sum-) "6c2ebd2e566677f8b421547f8e5266ee")
(setf (get rail_manipulation_msgs::PairwiseRankRequest :datatype-) "rail_manipulation_msgs/PairwiseRankRequest")
(setf (get rail_manipulation_msgs::PairwiseRankRequest :definition-)
      "
---
geometry_msgs/PoseArray grasp_list

================================================================================
MSG: geometry_msgs/PoseArray
# An array of poses with a header for global reference.

Header header

Pose[] poses

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of postion and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
")

(setf (get rail_manipulation_msgs::PairwiseRankResponse :md5sum-) "6c2ebd2e566677f8b421547f8e5266ee")
(setf (get rail_manipulation_msgs::PairwiseRankResponse :datatype-) "rail_manipulation_msgs/PairwiseRankResponse")
(setf (get rail_manipulation_msgs::PairwiseRankResponse :definition-)
      "
---
geometry_msgs/PoseArray grasp_list

================================================================================
MSG: geometry_msgs/PoseArray
# An array of poses with a header for global reference.

Header header

Pose[] poses

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: geometry_msgs/Pose
# A representation of pose in free space, composed of postion and orientation. 
Point position
Quaternion orientation

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

================================================================================
MSG: geometry_msgs/Quaternion
# This represents an orientation in free space in quaternion form.

float64 x
float64 y
float64 z
float64 w
")



(provide :rail_manipulation_msgs/PairwiseRank "6c2ebd2e566677f8b421547f8e5266ee")


