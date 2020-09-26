; Auto-generated. Do not edit!


(cl:in-package rail_manipulation_msgs-msg)


;//! \htmlinclude GraspFeedback.msg.html

(cl:defclass <GraspFeedback> (roslisp-msg-protocol:ros-message)
  ((indices_considered
    :reader indices_considered
    :initarg :indices_considered
    :type (cl:vector cl:integer)
   :initform (cl:make-array 0 :element-type 'cl:integer :initial-element 0))
   (index_selected
    :reader index_selected
    :initarg :index_selected
    :type cl:integer
    :initform 0))
)

(cl:defclass GraspFeedback (<GraspFeedback>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GraspFeedback>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GraspFeedback)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rail_manipulation_msgs-msg:<GraspFeedback> is deprecated: use rail_manipulation_msgs-msg:GraspFeedback instead.")))

(cl:ensure-generic-function 'indices_considered-val :lambda-list '(m))
(cl:defmethod indices_considered-val ((m <GraspFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rail_manipulation_msgs-msg:indices_considered-val is deprecated.  Use rail_manipulation_msgs-msg:indices_considered instead.")
  (indices_considered m))

(cl:ensure-generic-function 'index_selected-val :lambda-list '(m))
(cl:defmethod index_selected-val ((m <GraspFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rail_manipulation_msgs-msg:index_selected-val is deprecated.  Use rail_manipulation_msgs-msg:index_selected instead.")
  (index_selected m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GraspFeedback>) ostream)
  "Serializes a message object of type '<GraspFeedback>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'indices_considered))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let* ((signed ele) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    ))
   (cl:slot-value msg 'indices_considered))
  (cl:let* ((signed (cl:slot-value msg 'index_selected)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GraspFeedback>) istream)
  "Deserializes a message object of type '<GraspFeedback>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'indices_considered) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'indices_considered)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:aref vals i) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296)))))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'index_selected) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GraspFeedback>)))
  "Returns string type for a message object of type '<GraspFeedback>"
  "rail_manipulation_msgs/GraspFeedback")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GraspFeedback)))
  "Returns string type for a message object of type 'GraspFeedback"
  "rail_manipulation_msgs/GraspFeedback")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GraspFeedback>)))
  "Returns md5sum for a message object of type '<GraspFeedback>"
  "4e864dcbf0eb315180e735726b63001e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GraspFeedback)))
  "Returns md5sum for a message object of type 'GraspFeedback"
  "4e864dcbf0eb315180e735726b63001e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GraspFeedback>)))
  "Returns full string definition for message of type '<GraspFeedback>"
  (cl:format cl:nil "int32[] indices_considered           # indices of grasps seen by the user~%int32 index_selected                 # index of grasp selected for execution~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GraspFeedback)))
  "Returns full string definition for message of type 'GraspFeedback"
  (cl:format cl:nil "int32[] indices_considered           # indices of grasps seen by the user~%int32 index_selected                 # index of grasp selected for execution~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GraspFeedback>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'indices_considered) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GraspFeedback>))
  "Converts a ROS message object to a list"
  (cl:list 'GraspFeedback
    (cl:cons ':indices_considered (indices_considered msg))
    (cl:cons ':index_selected (index_selected msg))
))
