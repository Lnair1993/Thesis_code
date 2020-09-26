
(cl:in-package :asdf)

(defsystem "rail_segmentation-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "RemoveObject" :depends-on ("_package_RemoveObject"))
    (:file "_package_RemoveObject" :depends-on ("_package"))
  ))