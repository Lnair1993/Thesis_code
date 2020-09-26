;; Auto-generated. Do not edit!


(when (boundp 'kinova_msgs::ArmJointAnglesResult)
  (if (not (find-package "KINOVA_MSGS"))
    (make-package "KINOVA_MSGS"))
  (shadow 'ArmJointAnglesResult (find-package "KINOVA_MSGS")))
(unless (find-package "KINOVA_MSGS::ARMJOINTANGLESRESULT")
  (make-package "KINOVA_MSGS::ARMJOINTANGLESRESULT"))

(in-package "ROS")
;;//! \htmlinclude ArmJointAnglesResult.msg.html


(defclass kinova_msgs::ArmJointAnglesResult
  :super ros::object
  :slots (_angles ))

(defmethod kinova_msgs::ArmJointAnglesResult
  (:init
   (&key
    ((:angles __angles) (instance kinova_msgs::JointAngles :init))
    )
   (send-super :init)
   (setq _angles __angles)
   self)
  (:angles
   (&rest __angles)
   (if (keywordp (car __angles))
       (send* _angles __angles)
     (progn
       (if __angles (setq _angles (car __angles)))
       _angles)))
  (:serialization-length
   ()
   (+
    ;; kinova_msgs/JointAngles _angles
    (send _angles :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; kinova_msgs/JointAngles _angles
       (send _angles :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; kinova_msgs/JointAngles _angles
     (send _angles :deserialize buf ptr-) (incf ptr- (send _angles :serialization-length))
   ;;
   self)
  )

(setf (get kinova_msgs::ArmJointAnglesResult :md5sum-) "cadc8c9df1338a45563e10d707e71551")
(setf (get kinova_msgs::ArmJointAnglesResult :datatype-) "kinova_msgs/ArmJointAnglesResult")
(setf (get kinova_msgs::ArmJointAnglesResult :definition-)
      "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
# Result
JointAngles angles

================================================================================
MSG: kinova_msgs/JointAngles
float32 joint1
float32 joint2
float32 joint3
float32 joint4
float32 joint5
float32 joint6
float32 joint7

")



(provide :kinova_msgs/ArmJointAnglesResult "cadc8c9df1338a45563e10d707e71551")

