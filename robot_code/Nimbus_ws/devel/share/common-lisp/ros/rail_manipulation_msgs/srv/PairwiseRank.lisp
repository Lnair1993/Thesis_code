; Auto-generated. Do not edit!


(cl:in-package rail_manipulation_msgs-srv)


;//! \htmlinclude PairwiseRank-request.msg.html

(cl:defclass <PairwiseRank-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass PairwiseRank-request (<PairwiseRank-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PairwiseRank-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PairwiseRank-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rail_manipulation_msgs-srv:<PairwiseRank-request> is deprecated: use rail_manipulation_msgs-srv:PairwiseRank-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PairwiseRank-request>) ostream)
  "Serializes a message object of type '<PairwiseRank-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PairwiseRank-request>) istream)
  "Deserializes a message object of type '<PairwiseRank-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PairwiseRank-request>)))
  "Returns string type for a service object of type '<PairwiseRank-request>"
  "rail_manipulation_msgs/PairwiseRankRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PairwiseRank-request)))
  "Returns string type for a service object of type 'PairwiseRank-request"
  "rail_manipulation_msgs/PairwiseRankRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PairwiseRank-request>)))
  "Returns md5sum for a message object of type '<PairwiseRank-request>"
  "6c2ebd2e566677f8b421547f8e5266ee")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PairwiseRank-request)))
  "Returns md5sum for a message object of type 'PairwiseRank-request"
  "6c2ebd2e566677f8b421547f8e5266ee")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PairwiseRank-request>)))
  "Returns full string definition for message of type '<PairwiseRank-request>"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PairwiseRank-request)))
  "Returns full string definition for message of type 'PairwiseRank-request"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PairwiseRank-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PairwiseRank-request>))
  "Converts a ROS message object to a list"
  (cl:list 'PairwiseRank-request
))
;//! \htmlinclude PairwiseRank-response.msg.html

(cl:defclass <PairwiseRank-response> (roslisp-msg-protocol:ros-message)
  ((grasp_list
    :reader grasp_list
    :initarg :grasp_list
    :type geometry_msgs-msg:PoseArray
    :initform (cl:make-instance 'geometry_msgs-msg:PoseArray)))
)

(cl:defclass PairwiseRank-response (<PairwiseRank-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PairwiseRank-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PairwiseRank-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rail_manipulation_msgs-srv:<PairwiseRank-response> is deprecated: use rail_manipulation_msgs-srv:PairwiseRank-response instead.")))

(cl:ensure-generic-function 'grasp_list-val :lambda-list '(m))
(cl:defmethod grasp_list-val ((m <PairwiseRank-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rail_manipulation_msgs-srv:grasp_list-val is deprecated.  Use rail_manipulation_msgs-srv:grasp_list instead.")
  (grasp_list m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PairwiseRank-response>) ostream)
  "Serializes a message object of type '<PairwiseRank-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'grasp_list) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PairwiseRank-response>) istream)
  "Deserializes a message object of type '<PairwiseRank-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'grasp_list) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PairwiseRank-response>)))
  "Returns string type for a service object of type '<PairwiseRank-response>"
  "rail_manipulation_msgs/PairwiseRankResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PairwiseRank-response)))
  "Returns string type for a service object of type 'PairwiseRank-response"
  "rail_manipulation_msgs/PairwiseRankResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PairwiseRank-response>)))
  "Returns md5sum for a message object of type '<PairwiseRank-response>"
  "6c2ebd2e566677f8b421547f8e5266ee")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PairwiseRank-response)))
  "Returns md5sum for a message object of type 'PairwiseRank-response"
  "6c2ebd2e566677f8b421547f8e5266ee")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PairwiseRank-response>)))
  "Returns full string definition for message of type '<PairwiseRank-response>"
  (cl:format cl:nil "geometry_msgs/PoseArray grasp_list~%~%================================================================================~%MSG: geometry_msgs/PoseArray~%# An array of poses with a header for global reference.~%~%Header header~%~%Pose[] poses~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of postion and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PairwiseRank-response)))
  "Returns full string definition for message of type 'PairwiseRank-response"
  (cl:format cl:nil "geometry_msgs/PoseArray grasp_list~%~%================================================================================~%MSG: geometry_msgs/PoseArray~%# An array of poses with a header for global reference.~%~%Header header~%~%Pose[] poses~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of postion and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PairwiseRank-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'grasp_list))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PairwiseRank-response>))
  "Converts a ROS message object to a list"
  (cl:list 'PairwiseRank-response
    (cl:cons ':grasp_list (grasp_list msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'PairwiseRank)))
  'PairwiseRank-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'PairwiseRank)))
  'PairwiseRank-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PairwiseRank)))
  "Returns string type for a service object of type '<PairwiseRank>"
  "rail_manipulation_msgs/PairwiseRank")