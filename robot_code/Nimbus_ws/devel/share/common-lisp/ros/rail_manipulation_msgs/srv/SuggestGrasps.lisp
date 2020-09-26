; Auto-generated. Do not edit!


(cl:in-package rail_manipulation_msgs-srv)


;//! \htmlinclude SuggestGrasps-request.msg.html

(cl:defclass <SuggestGrasps-request> (roslisp-msg-protocol:ros-message)
  ((cloud
    :reader cloud
    :initarg :cloud
    :type sensor_msgs-msg:PointCloud2
    :initform (cl:make-instance 'sensor_msgs-msg:PointCloud2)))
)

(cl:defclass SuggestGrasps-request (<SuggestGrasps-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SuggestGrasps-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SuggestGrasps-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rail_manipulation_msgs-srv:<SuggestGrasps-request> is deprecated: use rail_manipulation_msgs-srv:SuggestGrasps-request instead.")))

(cl:ensure-generic-function 'cloud-val :lambda-list '(m))
(cl:defmethod cloud-val ((m <SuggestGrasps-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rail_manipulation_msgs-srv:cloud-val is deprecated.  Use rail_manipulation_msgs-srv:cloud instead.")
  (cloud m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SuggestGrasps-request>) ostream)
  "Serializes a message object of type '<SuggestGrasps-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'cloud) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SuggestGrasps-request>) istream)
  "Deserializes a message object of type '<SuggestGrasps-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'cloud) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SuggestGrasps-request>)))
  "Returns string type for a service object of type '<SuggestGrasps-request>"
  "rail_manipulation_msgs/SuggestGraspsRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SuggestGrasps-request)))
  "Returns string type for a service object of type 'SuggestGrasps-request"
  "rail_manipulation_msgs/SuggestGraspsRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SuggestGrasps-request>)))
  "Returns md5sum for a message object of type '<SuggestGrasps-request>"
  "2e99096b2d9e72ab0621b90ffe5e5f64")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SuggestGrasps-request)))
  "Returns md5sum for a message object of type 'SuggestGrasps-request"
  "2e99096b2d9e72ab0621b90ffe5e5f64")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SuggestGrasps-request>)))
  "Returns full string definition for message of type '<SuggestGrasps-request>"
  (cl:format cl:nil "sensor_msgs/PointCloud2 cloud~%~%================================================================================~%MSG: sensor_msgs/PointCloud2~%# This message holds a collection of N-dimensional points, which may~%# contain additional information such as normals, intensity, etc. The~%# point data is stored as a binary blob, its layout described by the~%# contents of the \"fields\" array.~%~%# The point cloud data may be organized 2d (image-like) or 1d~%# (unordered). Point clouds organized as 2d images may be produced by~%# camera depth sensors such as stereo or time-of-flight.~%~%# Time of sensor data acquisition, and the coordinate frame ID (for 3d~%# points).~%Header header~%~%# 2D structure of the point cloud. If the cloud is unordered, height is~%# 1 and width is the length of the point cloud.~%uint32 height~%uint32 width~%~%# Describes the channels and their layout in the binary data blob.~%PointField[] fields~%~%bool    is_bigendian # Is this data bigendian?~%uint32  point_step   # Length of a point in bytes~%uint32  row_step     # Length of a row in bytes~%uint8[] data         # Actual point data, size is (row_step*height)~%~%bool is_dense        # True if there are no invalid points~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: sensor_msgs/PointField~%# This message holds the description of one point entry in the~%# PointCloud2 message format.~%uint8 INT8    = 1~%uint8 UINT8   = 2~%uint8 INT16   = 3~%uint8 UINT16  = 4~%uint8 INT32   = 5~%uint8 UINT32  = 6~%uint8 FLOAT32 = 7~%uint8 FLOAT64 = 8~%~%string name      # Name of field~%uint32 offset    # Offset from start of point struct~%uint8  datatype  # Datatype enumeration, see above~%uint32 count     # How many elements in the field~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SuggestGrasps-request)))
  "Returns full string definition for message of type 'SuggestGrasps-request"
  (cl:format cl:nil "sensor_msgs/PointCloud2 cloud~%~%================================================================================~%MSG: sensor_msgs/PointCloud2~%# This message holds a collection of N-dimensional points, which may~%# contain additional information such as normals, intensity, etc. The~%# point data is stored as a binary blob, its layout described by the~%# contents of the \"fields\" array.~%~%# The point cloud data may be organized 2d (image-like) or 1d~%# (unordered). Point clouds organized as 2d images may be produced by~%# camera depth sensors such as stereo or time-of-flight.~%~%# Time of sensor data acquisition, and the coordinate frame ID (for 3d~%# points).~%Header header~%~%# 2D structure of the point cloud. If the cloud is unordered, height is~%# 1 and width is the length of the point cloud.~%uint32 height~%uint32 width~%~%# Describes the channels and their layout in the binary data blob.~%PointField[] fields~%~%bool    is_bigendian # Is this data bigendian?~%uint32  point_step   # Length of a point in bytes~%uint32  row_step     # Length of a row in bytes~%uint8[] data         # Actual point data, size is (row_step*height)~%~%bool is_dense        # True if there are no invalid points~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: sensor_msgs/PointField~%# This message holds the description of one point entry in the~%# PointCloud2 message format.~%uint8 INT8    = 1~%uint8 UINT8   = 2~%uint8 INT16   = 3~%uint8 UINT16  = 4~%uint8 INT32   = 5~%uint8 UINT32  = 6~%uint8 FLOAT32 = 7~%uint8 FLOAT64 = 8~%~%string name      # Name of field~%uint32 offset    # Offset from start of point struct~%uint8  datatype  # Datatype enumeration, see above~%uint32 count     # How many elements in the field~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SuggestGrasps-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'cloud))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SuggestGrasps-request>))
  "Converts a ROS message object to a list"
  (cl:list 'SuggestGrasps-request
    (cl:cons ':cloud (cloud msg))
))
;//! \htmlinclude SuggestGrasps-response.msg.html

(cl:defclass <SuggestGrasps-response> (roslisp-msg-protocol:ros-message)
  ((grasp_list
    :reader grasp_list
    :initarg :grasp_list
    :type geometry_msgs-msg:PoseArray
    :initform (cl:make-instance 'geometry_msgs-msg:PoseArray)))
)

(cl:defclass SuggestGrasps-response (<SuggestGrasps-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <SuggestGrasps-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'SuggestGrasps-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rail_manipulation_msgs-srv:<SuggestGrasps-response> is deprecated: use rail_manipulation_msgs-srv:SuggestGrasps-response instead.")))

(cl:ensure-generic-function 'grasp_list-val :lambda-list '(m))
(cl:defmethod grasp_list-val ((m <SuggestGrasps-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rail_manipulation_msgs-srv:grasp_list-val is deprecated.  Use rail_manipulation_msgs-srv:grasp_list instead.")
  (grasp_list m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <SuggestGrasps-response>) ostream)
  "Serializes a message object of type '<SuggestGrasps-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'grasp_list) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <SuggestGrasps-response>) istream)
  "Deserializes a message object of type '<SuggestGrasps-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'grasp_list) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<SuggestGrasps-response>)))
  "Returns string type for a service object of type '<SuggestGrasps-response>"
  "rail_manipulation_msgs/SuggestGraspsResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SuggestGrasps-response)))
  "Returns string type for a service object of type 'SuggestGrasps-response"
  "rail_manipulation_msgs/SuggestGraspsResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<SuggestGrasps-response>)))
  "Returns md5sum for a message object of type '<SuggestGrasps-response>"
  "2e99096b2d9e72ab0621b90ffe5e5f64")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'SuggestGrasps-response)))
  "Returns md5sum for a message object of type 'SuggestGrasps-response"
  "2e99096b2d9e72ab0621b90ffe5e5f64")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<SuggestGrasps-response>)))
  "Returns full string definition for message of type '<SuggestGrasps-response>"
  (cl:format cl:nil "geometry_msgs/PoseArray grasp_list~%~%================================================================================~%MSG: geometry_msgs/PoseArray~%# An array of poses with a header for global reference.~%~%Header header~%~%Pose[] poses~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of postion and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'SuggestGrasps-response)))
  "Returns full string definition for message of type 'SuggestGrasps-response"
  (cl:format cl:nil "geometry_msgs/PoseArray grasp_list~%~%================================================================================~%MSG: geometry_msgs/PoseArray~%# An array of poses with a header for global reference.~%~%Header header~%~%Pose[] poses~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Pose~%# A representation of pose in free space, composed of postion and orientation. ~%Point position~%Quaternion orientation~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%================================================================================~%MSG: geometry_msgs/Quaternion~%# This represents an orientation in free space in quaternion form.~%~%float64 x~%float64 y~%float64 z~%float64 w~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <SuggestGrasps-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'grasp_list))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <SuggestGrasps-response>))
  "Converts a ROS message object to a list"
  (cl:list 'SuggestGrasps-response
    (cl:cons ':grasp_list (grasp_list msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'SuggestGrasps)))
  'SuggestGrasps-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'SuggestGrasps)))
  'SuggestGrasps-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'SuggestGrasps)))
  "Returns string type for a service object of type '<SuggestGrasps>"
  "rail_manipulation_msgs/SuggestGrasps")