;; Auto-generated. Do not edit!


(when (boundp 'rail_segmentation::RemoveObject)
  (if (not (find-package "RAIL_SEGMENTATION"))
    (make-package "RAIL_SEGMENTATION"))
  (shadow 'RemoveObject (find-package "RAIL_SEGMENTATION")))
(unless (find-package "RAIL_SEGMENTATION::REMOVEOBJECT")
  (make-package "RAIL_SEGMENTATION::REMOVEOBJECT"))
(unless (find-package "RAIL_SEGMENTATION::REMOVEOBJECTREQUEST")
  (make-package "RAIL_SEGMENTATION::REMOVEOBJECTREQUEST"))
(unless (find-package "RAIL_SEGMENTATION::REMOVEOBJECTRESPONSE")
  (make-package "RAIL_SEGMENTATION::REMOVEOBJECTRESPONSE"))

(in-package "ROS")





(defclass rail_segmentation::RemoveObjectRequest
  :super ros::object
  :slots (_index ))

(defmethod rail_segmentation::RemoveObjectRequest
  (:init
   (&key
    ((:index __index) 0)
    )
   (send-super :init)
   (setq _index (round __index))
   self)
  (:index
   (&optional __index)
   (if __index (setq _index __index)) _index)
  (:serialization-length
   ()
   (+
    ;; uint32 _index
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint32 _index
       (write-long _index s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint32 _index
     (setq _index (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass rail_segmentation::RemoveObjectResponse
  :super ros::object
  :slots ())

(defmethod rail_segmentation::RemoveObjectResponse
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

(defclass rail_segmentation::RemoveObject
  :super ros::object
  :slots ())

(setf (get rail_segmentation::RemoveObject :md5sum-) "ad7b979103dbd563a352ef5270716728")
(setf (get rail_segmentation::RemoveObject :datatype-) "rail_segmentation/RemoveObject")
(setf (get rail_segmentation::RemoveObject :request) rail_segmentation::RemoveObjectRequest)
(setf (get rail_segmentation::RemoveObject :response) rail_segmentation::RemoveObjectResponse)

(defmethod rail_segmentation::RemoveObjectRequest
  (:response () (instance rail_segmentation::RemoveObjectResponse :init)))

(setf (get rail_segmentation::RemoveObjectRequest :md5sum-) "ad7b979103dbd563a352ef5270716728")
(setf (get rail_segmentation::RemoveObjectRequest :datatype-) "rail_segmentation/RemoveObjectRequest")
(setf (get rail_segmentation::RemoveObjectRequest :definition-)
      "uint32 index
---


")

(setf (get rail_segmentation::RemoveObjectResponse :md5sum-) "ad7b979103dbd563a352ef5270716728")
(setf (get rail_segmentation::RemoveObjectResponse :datatype-) "rail_segmentation/RemoveObjectResponse")
(setf (get rail_segmentation::RemoveObjectResponse :definition-)
      "uint32 index
---


")



(provide :rail_segmentation/RemoveObject "ad7b979103dbd563a352ef5270716728")


