; Auto-generated. Do not edit!


(cl:in-package rail_segmentation-srv)


;//! \htmlinclude RemoveObject-request.msg.html

(cl:defclass <RemoveObject-request> (roslisp-msg-protocol:ros-message)
  ((index
    :reader index
    :initarg :index
    :type cl:integer
    :initform 0))
)

(cl:defclass RemoveObject-request (<RemoveObject-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RemoveObject-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RemoveObject-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rail_segmentation-srv:<RemoveObject-request> is deprecated: use rail_segmentation-srv:RemoveObject-request instead.")))

(cl:ensure-generic-function 'index-val :lambda-list '(m))
(cl:defmethod index-val ((m <RemoveObject-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader rail_segmentation-srv:index-val is deprecated.  Use rail_segmentation-srv:index instead.")
  (index m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RemoveObject-request>) ostream)
  "Serializes a message object of type '<RemoveObject-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'index)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'index)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RemoveObject-request>) istream)
  "Deserializes a message object of type '<RemoveObject-request>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'index)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'index)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RemoveObject-request>)))
  "Returns string type for a service object of type '<RemoveObject-request>"
  "rail_segmentation/RemoveObjectRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RemoveObject-request)))
  "Returns string type for a service object of type 'RemoveObject-request"
  "rail_segmentation/RemoveObjectRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RemoveObject-request>)))
  "Returns md5sum for a message object of type '<RemoveObject-request>"
  "ad7b979103dbd563a352ef5270716728")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RemoveObject-request)))
  "Returns md5sum for a message object of type 'RemoveObject-request"
  "ad7b979103dbd563a352ef5270716728")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RemoveObject-request>)))
  "Returns full string definition for message of type '<RemoveObject-request>"
  (cl:format cl:nil "uint32 index~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RemoveObject-request)))
  "Returns full string definition for message of type 'RemoveObject-request"
  (cl:format cl:nil "uint32 index~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RemoveObject-request>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RemoveObject-request>))
  "Converts a ROS message object to a list"
  (cl:list 'RemoveObject-request
    (cl:cons ':index (index msg))
))
;//! \htmlinclude RemoveObject-response.msg.html

(cl:defclass <RemoveObject-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass RemoveObject-response (<RemoveObject-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <RemoveObject-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'RemoveObject-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name rail_segmentation-srv:<RemoveObject-response> is deprecated: use rail_segmentation-srv:RemoveObject-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <RemoveObject-response>) ostream)
  "Serializes a message object of type '<RemoveObject-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <RemoveObject-response>) istream)
  "Deserializes a message object of type '<RemoveObject-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<RemoveObject-response>)))
  "Returns string type for a service object of type '<RemoveObject-response>"
  "rail_segmentation/RemoveObjectResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RemoveObject-response)))
  "Returns string type for a service object of type 'RemoveObject-response"
  "rail_segmentation/RemoveObjectResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<RemoveObject-response>)))
  "Returns md5sum for a message object of type '<RemoveObject-response>"
  "ad7b979103dbd563a352ef5270716728")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'RemoveObject-response)))
  "Returns md5sum for a message object of type 'RemoveObject-response"
  "ad7b979103dbd563a352ef5270716728")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<RemoveObject-response>)))
  "Returns full string definition for message of type '<RemoveObject-response>"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'RemoveObject-response)))
  "Returns full string definition for message of type 'RemoveObject-response"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <RemoveObject-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <RemoveObject-response>))
  "Converts a ROS message object to a list"
  (cl:list 'RemoveObject-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'RemoveObject)))
  'RemoveObject-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'RemoveObject)))
  'RemoveObject-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'RemoveObject)))
  "Returns string type for a service object of type '<RemoveObject>"
  "rail_segmentation/RemoveObject")